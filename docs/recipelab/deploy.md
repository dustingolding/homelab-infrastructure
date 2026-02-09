# Deploy RecipeLab

## Build Images
- Build API image from `recipelab/api`.
- Build worker image from `recipelab/worker`.
- Build web image from `recipelab/web`.
- Push images to your preferred registry and update image references in `namespaces/recipelab/apps/recipelab-*.deployment.yaml`.
- Postgres uses `pgvector/pgvector:pg16` to ensure the `vector` extension is available.

## Secrets
- Edit `namespaces/recipelab/apps/recipelab-secrets.secret.sops.yaml` with real values.
- Encrypt the secret file with SOPS:
```bash
sops --encrypt --in-place namespaces/recipelab/apps/recipelab-secrets.secret.sops.yaml
```

## Apply via GitOps
- Commit changes to Git and let Flux reconcile `clusters/k3s-homelab`.
- Avoid manual `kubectl apply` on the live cluster.

## Verify
- Run `scripts/recipelab-smoke-test.sh` after Flux applies the changes.
