# Observability Namespace

## Overview (Manual)
This namespace contains observability agents responsible for collecting logs and telemetry from cluster workloads.

It currently runs Grafana Alloy as a DaemonSet on all nodes.

## Access (Manual)
There is no user-facing interface in this namespace.

Logs and telemetry are forwarded to Loki and Prometheus in the monitoring namespace.

Status can be inspected with:
```
kubectl -n observability get pods
kubectl -n observability logs <pod>
```

Upgrade example:
Upgrade order:
1. Telemetry agents (e.g., Alloy)

Before upgrades:
- Verify pipelines are healthy

Upgrades should be performed via Git commits, not kubectl apply directly.

Destroy / Rebuild
This namespace does not store persistent data.

Before destruction:
- Ensure no critical dashboards or pipelines depend on these components

Rebuild requires:
- Re-applying manifests
- Verifying telemetry pipelines

## Scheduling Notes (Manual)
Observability agents run on every node (DaemonSet).

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: observability
- purpose: Logging and telemetry pipelines for cluster services.
- exposure.type: internal
- exposure.ingress: none
- exposure.domains: none
- data.persistence: false
- data.components: alloy
- data.backup_required: false
- dependencies: ingress-nginx, monitoring
- criticality: medium
- rebuild_time_estimate: 15–30 minutes
- owners: dustin
Deployed services:
- none
Helm values:
- none
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
