# CMS Namespace

## Overview (Manual)
This namespace hosts WordPress-based CMS workloads intended for public-facing, monetized websites.

Each site is deployed using WordPress + MariaDB with Redis for caching. Ingress is handled via nginx and Cloudflare is used externally for DNS and edge protection.

## Access (Manual)
WordPress admin access is available at:
- https://<domain>/wp-admin

Authentication is handled internally by WordPress and Cloudflare rules. No SSO is currently configured.

Upgrade example:
Upgrade order:
1. WordPress application (Helm chart / image)
2. Redis (if required)
3. MariaDB ONLY after verified compatibility

Before upgrades:
- Verify MariaDB PVC is healthy
- Ensure backups exist

Upgrades should be performed via Git commits, not kubectl apply directly.

Destroy / Rebuild
This namespace contains persistent data.

Before destruction:
- Ensure MariaDB PVC backups exist
- Confirm WordPress uploads are backed up

Destroying the namespace without backups will result in data loss.

Rebuild requires:
- Re-applying manifests
- Restoring database and uploads

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: cms
- purpose: Public-facing WordPress workloads used for future monetized sites.
- exposure.type: public
- exposure.ingress: nginx
- exposure.domains: thealgoera.com, www.thealgoera.com
- data.persistence: true
- data.components: mariadb, redis
- data.backup_required: true
- dependencies: ingress-nginx, monitoring, observability
- criticality: medium
- rebuild_time_estimate: 30–60 minutes
- owners: dustin
Deployed services:
- CronJob/mariadb-backup
- CronJob/mariadb-restore-test
- CronJob/wordpress-backup
- CronJob/wp-cron
- Job/mariadb-restore-test
Helm values:
- values/mariadb.values.yaml
- values/redis.values.yaml
- values/wordpress.values.yaml
Helm images (values):
- none
Images & versions:
- alpine:3.20
- bitnami/mariadb:latest
- curlimages/curl:8.7.1
Ports / ingress:
- none
Resources:
- none
Dependencies:
- PVC/cms-backups-pvc
- PVC/cms-backups-wp-pvc
- PVC/wordpress
- Secret/mariadb
<!-- AUTO-GENERATED:END -->
