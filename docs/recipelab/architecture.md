# RecipeLab Architecture

## Overview
RecipeLab is deployed as a namespace-scoped application with separate components for web UI, API, worker, Postgres (with pgvector), and Redis.

## Components
- Web UI: Static site served by Nginx. Accessible via ingress at `recipelab.homelab.local`.
- API: FastAPI service providing ingestion, search, and chat endpoints.
- Worker: Background processor for ingestion, chunking, embedding, and web imports.
- Postgres: Primary data store with `pgvector` for semantic search.
- Redis: Queue and cache for background job dispatch.

## Data Flow
1. User uploads a recipe or requests a web import via the web UI.
2. API stores the raw recipe and creates an ingestion job.
3. Worker consumes the job, fetches content (if needed), chunks and embeds it, then stores vectors in Postgres.
4. Search and chat endpoints query embeddings for relevant recipe context.

## Networking
- Ingress: `traefik` with `recipelab.homelab.local` host.
- API and web services are exposed internally via ClusterIP.
- Postgres and Redis are internal only.

## Storage
- Postgres data is stored on a PVC using the `local-path` StorageClass.
- Redis is ephemeral in the current deployment.

## Security Boundaries
- OpenAI API keys are stored in SOPS-encrypted Kubernetes Secret.
- API enforces feature layers based on config flags.
- No browser-side OpenAI usage.
