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

## Scheduling Notes (Manual)
CMS workloads are intended to run on amd64 nodes only.

Preferred nodes:
- Proxmox VMs
- Bare metal servers

Raspberry Pi (ARM) nodes are excluded unless explicitly overridden.

Node labels used:
- node.platform=amd64
- node.type in {vm,baremetal}

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
- Deployment/wordpress
- Ingress/wordpress
- Job/mariadb-restore-test
- Service/mariadb
- Service/mariadb-headless
- Service/redis-headless
- Service/redis-master
- Service/redis-replicas
- Service/wordpress
- StatefulSet/mariadb
- StatefulSet/redis-master
- StatefulSet/redis-replicas
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
- registry-1.docker.io/bitnami/mariadb:latest
- registry-1.docker.io/bitnami/redis:latest
- registry-1.docker.io/bitnami/wordpress:latest
Ports / ingress:
- Ingress/wordpress: cms.thealgoera.com/
- Service/mariadb-headless: 3306/TCP -> mysql
- Service/mariadb: 3306/TCP -> mysql
- Service/redis-headless: 6379/TCP -> redis
- Service/redis-master: 6379/TCP -> redis
- Service/redis-replicas: 6379/TCP -> redis
- Service/wordpress: 443/TCP -> https
- Service/wordpress: 80/TCP -> http
Resources:
- mariadb: requests={'cpu': '500m', 'ephemeral-storage': '50Mi', 'memory': '512Mi'}, limits={'cpu': '750m', 'ephemeral-storage': '2Gi', 'memory': '768Mi'}
- prepare-base-dir: requests={'cpu': '300m', 'memory': '512Mi'}, limits={'cpu': '1000m', 'memory': '1024Mi'}
- preserve-logs-symlinks: requests={'cpu': '500m', 'ephemeral-storage': '50Mi', 'memory': '512Mi'}, limits={'cpu': '750m', 'ephemeral-storage': '2Gi', 'memory': '768Mi'}
- redis: requests={'cpu': '100m', 'ephemeral-storage': '50Mi', 'memory': '128Mi'}, limits={'cpu': '150m', 'ephemeral-storage': '2Gi', 'memory': '192Mi'}
- wordpress: requests={'cpu': '300m', 'memory': '512Mi'}, limits={'cpu': '1000m', 'memory': '1024Mi'}
Dependencies:
- ConfigMap/mariadb
- ConfigMap/redis-configuration
- ConfigMap/redis-health
- ConfigMap/redis-scripts
- PVC/cms-backups-pvc
- PVC/cms-backups-wp-pvc
- PVC/wordpress
- Secret/mariadb
- ServiceAccount/mariadb
- ServiceAccount/redis-master
- ServiceAccount/redis-replica
- ServiceAccount/wordpress
<!-- AUTO-GENERATED:END -->
