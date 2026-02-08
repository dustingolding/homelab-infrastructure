# Ingress-NGINX Namespace

## Overview (Manual)
This namespace runs the ingress-nginx controller that fronts HTTP/S traffic for the cluster.

It is the primary ingress path for public and internal services and must stay highly available.

## Access (Manual)
Ingress is accessed through the cluster’s edge IP(s) and DNS records. Admin access is via Kubernetes.

Upgrade example:
Upgrade order:
1. ingress-nginx controller

Before upgrades:
- Verify current ingress health and endpoints
- Ensure a rollback plan is available

Upgrades should be performed via Git commits, not kubectl apply directly.

Destroy / Rebuild
This namespace does not store persistent data.

Before destruction:
- Ensure no critical services depend on ingress routes

Rebuild requires:
- Re-applying manifests
- Verifying routes and certificates

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Metadata:
- namespace: ingress-nginx
- purpose: Ingress controller for cluster HTTP/S routing.
- exposure.type: public
- exposure.ingress: nginx
- exposure.domains: none
- data.persistence: false
- data.components: ingress-nginx
- data.backup_required: false
- dependencies: monitoring, observability
- criticality: high
- rebuild_time_estimate: 15–30 minutes
- owners: dustin
Deployed services:
- none
Helm values:
- values/ingress.values.yaml
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
