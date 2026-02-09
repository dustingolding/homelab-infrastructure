# RecipeLab Namespace

## Overview (Manual)
This namespace hosts RecipeLab, a local-network recipe ingestion, search, and AI-assisted cooking application.

It includes a web UI, API, background worker, Postgres (with pgvector), and Redis for queues/cache.

## Access (Manual)
RecipeLab UI is available at:
- http://recipelab.homelab.local

API access is routed under `/api` on the same host.

## Upgrades (Manual)
Upgrade order:
1. API + worker images
2. Web UI image
3. Postgres (only after backups and compatibility checks)
4. Redis (if required)

Upgrades should be performed via Git commits and Flux sync, not manual kubectl edits.

## Destroy / Rebuild (Manual)
This namespace contains persistent data.

Before destruction:
- Ensure Postgres backups exist
- Verify exported recipes and preferences

Rebuild requires:
- Re-applying manifests
- Restoring Postgres data

## Scheduling Notes (Manual)
RecipeLab workloads are intended to run on amd64 nodes only.

Node labels used:
- node.platform=amd64

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: recipelab
- purpose: Local-network RecipeLab application for recipe ingestion, search, and AI-assisted cooking workflows.
- exposure.type: internal
- exposure.ingress: traefik
- exposure.domains: recipelab.homelab.local
- data.persistence: true
- data.components: postgres, redis
- data.backup_required: true
- dependencies: monitoring, observability
- criticality: medium
- rebuild_time_estimate: 30–60 minutes
- owners: dustin
Deployed services:
- CronJob/recipelab-postgres-backup
- Deployment/recipelab-api
- Deployment/recipelab-redis
- Deployment/recipelab-web
- Deployment/recipelab-worker
- Ingress/recipelab
- Service/recipelab-api
- Service/recipelab-postgres
- Service/recipelab-redis
- Service/recipelab-web
- StatefulSet/recipelab-postgres
Helm values:
- none
Helm images (values):
- none
Images & versions:
- pgvector/pgvector:pg16
- postgres:16-alpine
- recipelab-api:0.1.0
- recipelab-web:0.1.0
- recipelab-worker:0.1.0
- redis:7.2-alpine
Ports / ingress:
- Ingress/recipelab: recipelab.homelab.local/
- Ingress/recipelab: recipelab.homelab.local/api
- Service/recipelab-api: 8000/TCP -> 8000
- Service/recipelab-postgres: 5432/TCP -> 5432
- Service/recipelab-redis: 6379/TCP -> 6379
- Service/recipelab-web: 80/TCP -> 80
Resources:
- api: requests={'cpu': '200m', 'memory': '256Mi'}, limits={'cpu': '1000m', 'memory': '1Gi'}
- postgres: requests={'cpu': '250m', 'memory': '512Mi'}, limits={'cpu': '1000m', 'memory': '2Gi'}
- redis: requests={'cpu': '50m', 'memory': '128Mi'}, limits={'cpu': '250m', 'memory': '256Mi'}
- web: requests={'cpu': '50m', 'memory': '64Mi'}, limits={'cpu': '250m', 'memory': '256Mi'}
- worker: requests={'cpu': '200m', 'memory': '256Mi'}, limits={'cpu': '1000m', 'memory': '1Gi'}
Dependencies:
- ConfigMap/recipelab-config
- PVC/recipelab-backups-pvc
- PVC/recipelab-postgres-pvc
- Secret/recipelab-secrets
<!-- AUTO-GENERATED:END -->
