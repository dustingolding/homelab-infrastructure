# RecipeLab API

Base URL:
- Internal: `http://recipelab-api.recipelab.svc.cluster.local:8000`
- Ingress: `http://recipelab.homelab.local/api`

## Health
- `GET /healthz`
  - Returns `{"status":"ok"}`
- `GET /readyz`
  - Returns `{"status":"ready"}` or HTTP 503 if DB unavailable.

## Metrics
- `GET /metrics`
  - Prometheus format metrics.

## Ingestion
- `POST /recipes/import`
  - Form fields: `file` (optional), `content` (optional), `url` (optional), `title` (optional), `user_id` (optional)
  - At least one of `file`, `content`, or `url` is required.
  - Response: job and recipe identifiers.

## Search
- `GET /recipes/search?q=...&limit=5`
  - Returns semantic matches using pgvector.

## Chat
- `POST /chat`
  - Form fields: `message` (required), `user_id` (optional), `layers` (optional, comma-separated)
  - Enforces feature layer gating based on `RECIPES_FEATURE_*` flags.

## Examples
```bash
curl -fsS http://recipelab.homelab.local/api/healthz
curl -fsS -X POST -F "content=1 cup flour" http://recipelab.homelab.local/api/recipes/import
curl -fsS "http://recipelab.homelab.local/api/recipes/search?q=flour"
```
