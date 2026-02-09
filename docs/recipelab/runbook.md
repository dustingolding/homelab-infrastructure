# RecipeLab Runbook

## Deploy
1. Build and push API, worker, and web images.
2. Update image tags in `namespaces/recipelab/apps/` manifests.
3. Encrypt secrets with SOPS.
4. Commit and let Flux reconcile.

## Rollback
1. Revert the commit that updated manifests or images.
2. Push and allow Flux to reconcile.

## Scale
- Update `replicas` in the API and worker deployments.
- Do not scale Postgres beyond 1 without a dedicated HA plan.

## Rotate Secrets
1. Update `recipelab-secrets.secret.sops.yaml` with new values.
2. Re-encrypt via SOPS.
3. Commit and allow Flux to reconcile.

## Validate
- Run `scripts/recipelab-smoke-test.sh`.
- Confirm ingress resolves and UI loads.

## Upgrade Postgres
1. Ensure backups exist.
2. Update the Postgres image if needed.
3. Monitor readiness and logs.

## Common Commands
```bash
kubectl -n recipelab get pods
kubectl -n recipelab logs deployment/recipelab-api
kubectl -n recipelab logs deployment/recipelab-worker
kubectl -n recipelab logs deployment/recipelab-redis
kubectl -n recipelab logs statefulset/recipelab-postgres
```
