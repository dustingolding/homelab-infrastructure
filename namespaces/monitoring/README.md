# Monitoring Namespace

## Overview (Manual)
This namespace contains the monitoring stack for the Kubernetes cluster.

It includes Prometheus for metrics collection, Grafana for visualization, and Loki for log aggregation.

## Access (Manual)
Grafana is accessible via:
- http://grafana.homelab.local

Authentication:
- Grafana local users
- Admin credentials stored as Kubernetes secrets

If ingress is unavailable, Grafana can be accessed via port-forward:
```
kubectl -n monitoring port-forward svc/grafana 3000:80
```

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
- exposure.domains: grafana.homelab.local
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
