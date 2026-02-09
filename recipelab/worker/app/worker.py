import os
import time
import uuid
from typing import Any

import requests
from bs4 import BeautifulSoup

from .db import ensure_schema, get_conn
from .openai_client import OpenAIClient
from .queue import Queue


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if not text:
        return []
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        if overlap > 0:
            start = max(end - overlap, 0)
        else:
            start = end
    return [c.strip() for c in chunks if c.strip()]


def fetch_url(url: str) -> str:
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return "\n".join(s.strip() for s in soup.get_text("\n").splitlines() if s.strip())


def mark_job(job_id: str, status: str, detail: str | None = None) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE ingestion_jobs SET status=%s, detail=%s, updated_at=NOW() WHERE id=%s",
                (status, detail, job_id),
            )
        conn.commit()


def upsert_recipe(recipe_id: str, content: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE recipes SET content=%s WHERE id=%s", (content, recipe_id))
        conn.commit()


def insert_chunks(recipe_id: str, chunks: list[str]) -> None:
    client = OpenAIClient()
    embeddings = client.embed_texts(chunks)
    with get_conn() as conn:
        with conn.cursor() as cur:
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=False)):
                cur.execute(
                    """
                    INSERT INTO recipe_chunks (id, recipe_id, chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (str(uuid.uuid4()), recipe_id, idx, chunk, embedding),
                )
        conn.commit()


def handle_job(job: dict[str, Any]) -> None:
    job_type = job.get("job_type")
    payload = job.get("payload", {})
    job_id = payload.get("job_id")
    recipe_id = payload.get("recipe_id")
    if not job_id or not recipe_id:
        return

    try:
        mark_job(job_id, "running", job_type)
        content = payload.get("content") or ""
        if job_type == "web_import":
            url = payload.get("url")
            if not url:
                raise RuntimeError("Missing url for web_import")
            content = fetch_url(url)
        if not content:
            raise RuntimeError("No content to process")

        chunk_size = int(os.getenv("RECIPES_CHUNK_SIZE", "800"))
        overlap = int(os.getenv("RECIPES_CHUNK_OVERLAP", "100"))
        chunks = chunk_text(content, chunk_size, overlap)
        upsert_recipe(recipe_id, content)
        insert_chunks(recipe_id, chunks)
        mark_job(job_id, "complete", f"chunks={len(chunks)}")
    except Exception as exc:  # noqa: BLE001
        mark_job(job_id, "failed", str(exc))


def run() -> None:
    ensure_schema()
    queue = Queue()
    while True:
        job = queue.pop(timeout=5)
        if job:
            handle_job(job)
        else:
            time.sleep(1)


if __name__ == "__main__":
    run()
