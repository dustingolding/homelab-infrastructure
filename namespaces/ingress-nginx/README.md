# Ingress-NGINX Namespace

## Overview (Manual)
This namespace provides the cluster-wide Ingress controller based on ingress-nginx.

All external HTTP/S traffic into the cluster flows through this component before being routed to application namespaces.

## Access (Manual)
The ingress controller does not expose a user interface.

Traffic enters the cluster via the LoadBalancer services created by ingress-nginx and is routed to applications based on Ingress resources.

Ingress status can be inspected with:
```
kubectl -n ingress-nginx get svc
kubectl -n ingress-nginx get pods
```

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
- exposure.type: internal
- exposure.ingress: self
- exposure.domains: none
- data.persistence: false
- data.components: ingress-nginx
- data.backup_required: false
- dependencies: monitoring, observability
- criticality: high
- rebuild_time_estimate: 15–30 minutes
- owners: dustin
Deployed services:
- Deployment/ingress-ingress-nginx-controller
- Service/ingress-ingress-nginx-controller
Helm values:
- values/ingress.values.yaml
Helm images (values):
- none
Images & versions:
- registry.k8s.io/ingress-nginx/controller:v1.14.3@sha256:82917be97c0939f6ada1717bb39aa7e66c229d6cfb10dcfc8f1bd42f9efe0f81
Ports / ingress:
- Service/ingress-ingress-nginx-controller: 443/TCP -> https
- Service/ingress-ingress-nginx-controller: 80/TCP -> http
Resources:
- controller: requests={'cpu': '100m', 'memory': '90Mi'}
Dependencies:
- ServiceAccount/ingress-ingress-nginx
<!-- AUTO-GENERATED:END -->
