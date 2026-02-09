# RecipeLab Configuration

## ConfigMap: `recipelab-config`
- `APP_ENV`: runtime environment (default `production`).
- `LOG_LEVEL`: logging level (default `info`).
- `OPENAI_EMBED_MODEL`: embeddings model name (example `text-embedding-3-small`).
- `OPENAI_CHAT_MODEL`: chat model name (example `gpt-4o-mini`).
- `OPENAI_REQUEST_TIMEOUT_SECS`: OpenAI request timeout in seconds.
- `OPENAI_MAX_RETRIES`: OpenAI request retry count.
- `RECIPES_EMBEDDING_DIM`: embedding vector dimension (must match model).
- `RECIPES_CHUNK_SIZE`: chunk size for recipe ingestion.
- `RECIPES_CHUNK_OVERLAP`: chunk overlap for ingestion.
- `RECIPES_FEATURE_PANTRY`: enable pantry layer (`true`/`false`).
- `RECIPES_FEATURE_MEAL_PLANNING`: enable meal planning layer.
- `RECIPES_FEATURE_NUTRITION`: enable nutrition layer.
- `RECIPES_FEATURE_TEACHING`: enable teaching layer.
- `RECIPES_FEATURE_CREATIVE_REMIX`: enable creative remix layer.
- `RECIPES_FEATURE_SHOPPING_LISTS`: enable shopping list layer.
- `RECIPES_JOB_QUEUE`: Redis list name for jobs.
- `POSTGRES_HOST`: Postgres service hostname.
- `POSTGRES_PORT`: Postgres service port.
- `REDIS_HOST`: Redis service hostname.
- `REDIS_PORT`: Redis service port.

## Secret: `recipelab-secrets`
- `OPENAI_API_KEY`: OpenAI API key (required by API and worker).
- `POSTGRES_USER`: Postgres username.
- `POSTGRES_PASSWORD`: Postgres password.
- `POSTGRES_DB`: Postgres database name.
- `REDIS_PASSWORD`: Redis password.
- `SESSION_SECRET`: API session secret.

## Notes
- Update `OPENAI_*` model names via ConfigMap. Do not hardcode models in code.
- All secrets must remain encrypted with SOPS (`*.sops.yaml`).
