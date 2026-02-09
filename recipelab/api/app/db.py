import os
from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg_pool import ConnectionPool
from pgvector.psycopg import register_vector


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    if value is None:
        return None
    return value.strip()


def build_dsn() -> str:
    host = _env("POSTGRES_HOST", "recipelab-postgres")
    port = _env("POSTGRES_PORT", "5432")
    user = _env("POSTGRES_USER")
    password = _env("POSTGRES_PASSWORD")
    db = _env("POSTGRES_DB", "recipelab")
    if not user or not password:
        raise RuntimeError("POSTGRES_USER and POSTGRES_PASSWORD must be set")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


_POOL: ConnectionPool | None = None


def init_pool() -> ConnectionPool:
    global _POOL
    if _POOL is None:
        dsn = build_dsn()
        _POOL = ConnectionPool(conninfo=dsn, min_size=1, max_size=5, timeout=30)
    return _POOL


@contextmanager
def get_conn() -> Iterator[psycopg.Connection]:
    pool = init_pool()
    with pool.connection() as conn:
        register_vector(conn)
        yield conn


def ensure_schema() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS recipes (
                    id UUID PRIMARY KEY,
                    title TEXT NOT NULL,
                    source TEXT,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS recipe_chunks (
                    id UUID PRIMARY KEY,
                    recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
                    chunk_index INT NOT NULL,
                    content TEXT NOT NULL,
                    embedding VECTOR(%s),
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """,
                (int(_env("RECIPES_EMBEDDING_DIM", "1536")),),
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ingestion_jobs (
                    id UUID PRIMARY KEY,
                    recipe_id UUID,
                    source TEXT,
                    status TEXT NOT NULL,
                    detail TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    updated_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id UUID PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    rules JSONB NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS pantry_items (
                    id UUID PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    item TEXT NOT NULL,
                    quantity TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id UUID PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    context JSONB NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS substitution_history (
                    id UUID PRIMARY KEY,
                    recipe_id UUID,
                    from_ingredient TEXT NOT NULL,
                    to_ingredient TEXT NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
        conn.commit()
