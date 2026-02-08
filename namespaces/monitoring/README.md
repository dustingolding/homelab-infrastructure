# Monitoring Namespace

## Overview (Manual)
This namespace contains monitoring and alerting services for cluster health and application visibility.

It typically includes Prometheus, Grafana, and supporting components.

## Access (Manual)
Access is internal. Dashboards are exposed via ingress on internal domains and require authentication.

Upgrade example:
Upgrade order:
1. Grafana
2. Prometheus stack
3. Loki (if present)

Before upgrades:
- Verify persistent storage health
- Ensure backups exist

Upgrades should be performed via Git commits, not kubectl apply directly.

Destroy / Rebuild
This namespace contains persistent data.

Before destruction:
- Ensure Prometheus/Grafana/Loki data is backed up

Rebuild requires:
- Re-applying manifests
- Restoring persistent data if required

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: monitoring
- purpose: Metrics, alerting, and dashboards for cluster health.
- exposure.type: internal
- exposure.ingress: nginx
- exposure.domains: none
- data.persistence: true
- data.components: prometheus, grafana, loki
- data.backup_required: true
- dependencies: ingress-nginx, observability
- criticality: high
- rebuild_time_estimate: 30–60 minutes
- owners: dustin
Deployed services:
- none
Helm values:
- values/alloy.values.yaml
- values/grafana.values.yaml
- values/loki.values.yaml
- values/prometheus.values.yaml
Helm images (values):
- none
Images & versions:
- none
Ports / ingress:
- none
Resources:
- none
Dependencies:
- none
<!-- AUTO-GENERATED:END -->
