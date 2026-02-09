import os
import uuid
from typing import Any

import json

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest

from .db import ensure_schema, get_conn
from .openai_client import OpenAIClient
from .queue import Job, Queue

app = FastAPI(title="RecipeLab API", version="0.1.0")

REQUESTS = Counter("recipelab_api_requests_total", "Total API requests", ["path", "method"])
READY = Gauge("recipelab_api_ready", "Readiness status")


@app.on_event("startup")
def _startup() -> None:
    ensure_schema()


@app.middleware("http")
async def _metrics(request, call_next):  # type: ignore[override]
    response = await call_next(request)
    REQUESTS.labels(path=request.url.path, method=request.method).inc()
    return response


def _features_from_env() -> dict[str, bool]:
    def flag(name: str) -> bool:
        return os.getenv(name, "false").lower() == "true"

    return {
        "pantry": flag("RECIPES_FEATURE_PANTRY"),
        "meal_planning": flag("RECIPES_FEATURE_MEAL_PLANNING"),
        "nutrition": flag("RECIPES_FEATURE_NUTRITION"),
        "teaching": flag("RECIPES_FEATURE_TEACHING"),
        "creative_remix": flag("RECIPES_FEATURE_CREATIVE_REMIX"),
        "shopping_lists": flag("RECIPES_FEATURE_SHOPPING_LISTS"),
    }


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        READY.set(1)
        return {"status": "ready"}
    except Exception as exc:  # noqa: BLE001
        READY.set(0)
        raise HTTPException(status_code=503, detail=str(exc))


@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/recipes/import")
async def import_recipe(
    file: UploadFile | None = File(default=None),
    url: str | None = Form(default=None),
    title: str | None = Form(default=None),
    content: str | None = Form(default=None),
    user_id: str | None = Form(default="local"),
) -> dict[str, Any]:
    if not any([file, url, content]):
        raise HTTPException(status_code=400, detail="file, url, or content is required")

    source = None
    body = None
    job_type = "parse_import"

    if file is not None:
        raw = await file.read()
        body = raw.decode("utf-8", errors="ignore")
        source = file.filename
        title = title or file.filename
    elif content:
        body = content
        source = "manual"
    elif url:
        source = url
        job_type = "web_import"

    recipe_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO recipes (id, title, source, content) VALUES (%s, %s, %s, %s)",
                (recipe_id, title or "Untitled", source, body or ""),
            )
            cur.execute(
                "INSERT INTO ingestion_jobs (id, recipe_id, source, status, detail) VALUES (%s, %s, %s, %s, %s)",
                (job_id, recipe_id, source, "queued", job_type),
            )
        conn.commit()

    queue = Queue()
    queue.enqueue(
        Job(
            job_type=job_type,
            payload={
                "job_id": job_id,
                "recipe_id": recipe_id,
                "user_id": user_id,
                "title": title,
                "source": source,
                "content": body,
                "url": url,
            },
        )
    )

    return {"job_id": job_id, "recipe_id": recipe_id, "status": "queued"}


@app.get("/recipes/search")
def search_recipes(q: str, limit: int = 5) -> dict[str, Any]:
    client = OpenAIClient()
    embedding = client.embed_texts([q])[0]
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT recipes.id, recipes.title, recipes.source, recipe_chunks.content
                FROM recipe_chunks
                JOIN recipes ON recipes.id = recipe_chunks.recipe_id
                ORDER BY recipe_chunks.embedding <-> %s
                LIMIT %s
                """,
                (embedding, limit),
            )
            rows = cur.fetchall()
    results = [
        {"recipe_id": r[0], "title": r[1], "source": r[2], "chunk": r[3]} for r in rows
    ]
    return {"query": q, "results": results}


@app.post("/preferences")
def save_preferences(user_id: str = Form("local"), rules: str = Form(...)) -> dict[str, Any]:
    try:
        parsed = json.loads(rules)
        if not isinstance(parsed, dict):
            parsed = {"rules": parsed}
    except json.JSONDecodeError:
        parsed = {"rules": rules}

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_preferences (id, user_id, rules) VALUES (%s, %s, %s)",
                (str(uuid.uuid4()), user_id, json.dumps(parsed)),
            )
        conn.commit()
    return {"status": "saved"}


@app.get("/preferences")
def get_preferences(user_id: str = "local") -> dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT rules FROM user_preferences WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,),
            )
            row = cur.fetchone()
    return {"user_id": user_id, "rules": row[0] if row else {}}


@app.post("/pantry")
def save_pantry(user_id: str = Form("local"), items: str = Form(...)) -> dict[str, Any]:
    entries = [i.strip() for i in items.splitlines() if i.strip()]
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pantry_items WHERE user_id = %s", (user_id,))
            for item in entries:
                cur.execute(
                    "INSERT INTO pantry_items (id, user_id, item) VALUES (%s, %s, %s)",
                    (str(uuid.uuid4()), user_id, item),
                )
        conn.commit()
    return {"status": "saved", "count": len(entries)}


@app.get("/pantry")
def get_pantry(user_id: str = "local") -> dict[str, Any]:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT item, quantity FROM pantry_items WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,),
            )
            rows = cur.fetchall()
    items = [{"item": r[0], "quantity": r[1]} for r in rows]
    return {"user_id": user_id, "items": items}


@app.post("/chat")
def chat(message: str = Form(...), user_id: str = Form("local"), layers: str | None = Form(None)) -> dict[str, Any]:
    client = OpenAIClient()
    requested_layers = set()
    if layers:
        requested_layers = {l.strip() for l in layers.split(",") if l.strip()}

    feature_flags = _features_from_env()
    enabled_layers = sorted([k for k in requested_layers if feature_flags.get(k, False)])

    embedding = client.embed_texts([message])[0]
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT recipe_chunks.content
                FROM recipe_chunks
                ORDER BY recipe_chunks.embedding <-> %s
                LIMIT 5
                """,
                (embedding,),
            )
            chunks = [r[0] for r in cur.fetchall()]
            cur.execute(
                "SELECT rules FROM user_preferences WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
                (user_id,),
            )
            pref = cur.fetchone()

    prefs = pref[0] if pref else {}

    system_prompt = (
        "You are RecipeLab, a helpful cooking assistant. Use the provided recipe context to answer. "
        "Always prioritize user preferences and house rules."
    )
    if enabled_layers:
        system_prompt += f" Optional layers enabled: {', '.join(enabled_layers)}."

    context_block = "\n\n".join(chunks)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"User preferences: {prefs}"},
        {"role": "system", "content": f"Recipe context:\n{context_block}"},
        {"role": "user", "content": message},
    ]

    response = client.chat(messages)
    return {"response": response, "layers": enabled_layers}
