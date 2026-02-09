# RecipeLab Troubleshooting

## API not ready
- Check Postgres readiness and secret values.
- Verify `POSTGRES_*` values in the Secret.
- Inspect logs:
```bash
kubectl -n recipelab logs deployment/recipelab-api
```

## Worker not processing jobs
- Check Redis connectivity and password.
- Inspect worker logs:
```bash
kubectl -n recipelab logs deployment/recipelab-worker
```

## Ingress not reachable
- Confirm ingress IP exists:
```bash
kubectl -n recipelab get ingress recipelab
```
- Verify DNS or local hosts entry for `recipelab.homelab.local`.

## Embeddings failing
- Ensure OpenAI API key is set in the Secret.
- Verify outbound connectivity from the cluster.
- Check OpenAI rate limits and error responses in worker logs.

## Search returns empty
- Confirm ingestion jobs completed.
- Inspect `ingestion_jobs` table for status.
- Verify `pgvector` extension is available in Postgres.
