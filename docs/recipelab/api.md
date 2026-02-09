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

## Preferences
- `POST /preferences`
  - Form fields: `user_id` (optional), `rules` (required, JSON or plain text)
- `GET /preferences?user_id=...`
  - Returns latest stored preferences for a user.

## Pantry
- `POST /pantry`
  - Form fields: `user_id` (optional), `items` (required, newline-separated)
- `GET /pantry?user_id=...`
  - Returns stored pantry items for a user.

## Examples
```bash
curl -fsS http://recipelab.homelab.local/api/healthz
curl -fsS -X POST -F "content=1 cup flour" http://recipelab.homelab.local/api/recipes/import
curl -fsS "http://recipelab.homelab.local/api/recipes/search?q=flour"
curl -fsS -X POST -F "rules={\"no_peanuts\":true}" http://recipelab.homelab.local/api/preferences
curl -fsS -X POST -F $'items=rice\\nbeans\\nolive oil' http://recipelab.homelab.local/api/pantry
```
