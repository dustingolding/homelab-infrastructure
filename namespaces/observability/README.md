# Observability Namespace

## Overview (Manual)
This namespace contains telemetry and logging pipeline components used by the cluster.

## Access (Manual)
Access is internal via Kubernetes or internal ingress endpoints where applicable.

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

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: observability
- purpose: Logging and telemetry pipelines for cluster services.
- exposure.type: internal
- exposure.ingress: nginx
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
