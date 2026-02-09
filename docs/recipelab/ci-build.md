# RecipeLab CI and Build

## Build Targets
- API image: `recipelab/api`
- Worker image: `recipelab/worker`
- Web image: `recipelab/web`

## Image Tagging
- Use a consistent tag strategy (for example: `0.1.0`, `2026-02-09`, or git SHA).
- Update tags in `namespaces/recipelab/apps/recipelab-*.deployment.yaml`.

## Local Build Example
```bash
docker build -t recipelab-api:0.1.0 recipelab/api
docker build -t recipelab-worker:0.1.0 recipelab/worker
docker build -t recipelab-web:0.1.0 recipelab/web
```

## Publish
- Push to your preferred registry.
- Update manifests to match registry image references.
