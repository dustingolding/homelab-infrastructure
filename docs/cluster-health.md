# Cluster Health Snapshot

Date: 2026-02-10

## Nodes
- k3s-cp1 (control-plane) — Ready
- k3s-w1 — Ready
- k3s-w2 — Ready
- k3s-w3 — Ready
- k3s-w4 — Ready
- k3s-baremetal-01 — Ready

## Ingress
- ingress-nginx controller: Running
- Admission jobs: Completed and cleaned
- CMS ingress: `cms.thealgoera.com` (nginx)
- Grafana ingress: `grafana.homelab.local` (traefik)
- RecipeLab ingress: `recipelab.homelab.local` (traefik)

## CMS
- mariadb: Running
- redis: Running
- wordpress: Running
- wp-cron: Completed
- backups: Completed

## Monitoring
- grafana: Running
- prometheus: Running
- loki: Running
- alloy: Running

## RecipeLab
- api: Running
- web: Running
- worker: Running
- postgres: Running
- redis: Running

## Notes
- Live-cluster diff check passed after aligning WordPress PVC existingClaim and ingress admission webhook behavior.
