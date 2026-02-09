# RecipeLab Backups

## Postgres
- Postgres stores recipes, embeddings, preferences, and job records.
- Use a consistent backup strategy aligned with cluster conventions.

## CronJob
- `namespaces/recipelab/backups/recipelab-postgres-backup.cronjob.yaml` runs nightly backups.
- Backups are stored in `recipelab-backups-pvc`.

## Suggested Backup Flow
1. Create a logical backup with `pg_dump`.
2. Store backups in the existing backups system (or a dedicated PVC if needed).

Example:
```bash
kubectl -n recipelab exec statefulset/recipelab-postgres -- \
  pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > recipelab-$(date +%F).sql
```

## Restore
1. Create the database and user if needed.
2. Restore from the backup file.

Example:
```bash
kubectl -n recipelab exec -i statefulset/recipelab-postgres -- \
  psql -U "$POSTGRES_USER" "$POSTGRES_DB" < recipelab-YYYY-MM-DD.sql
```

## Notes
- Ensure backups are taken before schema changes or upgrades.
- Redis data is ephemeral and not backed up in the current deployment.
