# CMS Migration: Bitnami -> Docker Official Images

This plan migrates WordPress/MariaDB/Redis from Bitnami Helm charts to raw manifests using Docker Official images.

## Goals
- Remove dependency on Bitnami images and chart updates.
- Keep service names and PVCs intact.
- Preserve data.

## Pre-Checks
- Ensure WordPress is healthy in the current stack.
- Confirm backups exist (DB + wp-content).

## Step 1: Export current secrets
We will reuse the current secret values.

```bash
# MariaDB secrets
kubectl -n cms get secret mariadb -o jsonpath='{.data.mariadb-root-password}' | base64 -d
kubectl -n cms get secret mariadb -o jsonpath='{.data.mariadb-user}' | base64 -d
kubectl -n cms get secret mariadb -o jsonpath='{.data.mariadb-password}' | base64 -d
kubectl -n cms get secret mariadb -o jsonpath='{.data.mariadb-database}' | base64 -d

# WordPress secrets
kubectl -n cms get secret wordpress -o jsonpath='{.data.wordpress-username}' | base64 -d
kubectl -n cms get secret wordpress -o jsonpath='{.data.wordpress-password}' | base64 -d
kubectl -n cms get secret wordpress -o jsonpath='{.data.redis-password}' | base64 -d
```

## Step 2: Fill SOPS secrets
Edit:
- `namespaces/cms/apps/mariadb.secret.sops.yaml`
- `namespaces/cms/apps/wordpress.secret.sops.yaml`

Replace `REPLACE_ME` with the exported values, then encrypt:

```bash
sops --encrypt --in-place namespaces/cms/apps/mariadb.secret.sops.yaml
sops --encrypt --in-place namespaces/cms/apps/wordpress.secret.sops.yaml
```

## Step 3: Commit + merge
Commit the secret updates and merge the PR. Flux will then apply the manifests.

## Step 4: Cutover (maintenance window)
1. Pause Helm releases:

```bash
helm -n cms uninstall wordpress
helm -n cms uninstall mariadb
helm -n cms uninstall redis
```

2. Reconcile Flux:

```bash
flux reconcile source git homelab-infrastructure -n flux-system
flux reconcile kustomization k3s-homelab -n flux-system
```

3. Watch pods:

```bash
kubectl -n cms get pods -w
```

## Step 5: Validate
- `curl -I https://cms.thealgoera.com/wp-admin/`
- Login and verify posts/media.
- Check DB connectivity and Redis cache plugin.

## Rollback
If something fails:
1. Delete the new deployments/statefulset.
2. Reinstall Bitnami Helm charts with the previous values.

