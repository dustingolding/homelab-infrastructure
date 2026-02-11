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

## Scheduling Notes (Manual)
Monitoring workloads are intended to run on amd64 nodes.

Preferred nodes:
- Proxmox VMs
- Bare metal servers

Raspberry Pi nodes are allowed only for log shippers.

Node labels used:
- node.platform=amd64

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
- DaemonSet/alloy
- DaemonSet/loki-canary
- DaemonSet/prometheus-prometheus-node-exporter
- Deployment/grafana
- Deployment/loki-gateway
- Deployment/prometheus-kube-prometheus-operator
- Deployment/prometheus-kube-state-metrics
- Ingress/grafana
- Job/prometheus-kube-prometheus-admission-create
- Job/prometheus-kube-prometheus-admission-patch
- Service/alloy
- Service/grafana
- Service/loki
- Service/loki-canary
- Service/loki-gateway
- Service/loki-headless
- Service/loki-memberlist
- Service/loki-results-cache
- Service/prometheus-kube-prometheus-coredns
- Service/prometheus-kube-prometheus-kube-controller-manager
- Service/prometheus-kube-prometheus-kube-etcd
- Service/prometheus-kube-prometheus-kube-proxy
- Service/prometheus-kube-prometheus-kube-scheduler
- Service/prometheus-kube-prometheus-operator
- Service/prometheus-kube-prometheus-prometheus
- Service/prometheus-kube-state-metrics
- Service/prometheus-operated
- Service/prometheus-prometheus-node-exporter
- StatefulSet/loki
- StatefulSet/loki-results-cache
Helm values:
- values/alloy.values.yaml
- values/grafana.values.yaml
- values/loki.values.yaml
- values/prometheus.values.yaml
Helm images (values):
- none
Images & versions:
- docker.io/curlimages/curl:8.9.1
- docker.io/grafana/alloy:v1.12.2
- docker.io/grafana/grafana:12.3.1
- docker.io/grafana/loki-canary:3.6.4
- docker.io/grafana/loki:3.6.4
- docker.io/kiwigrid/k8s-sidecar:1.30.9
- docker.io/library/busybox:1.31.1
- docker.io/nginxinc/nginx-unprivileged:1.29-alpine
- ghcr.io/jkroepke/kube-webhook-certgen:1.7.4
- memcached:1.6.39-alpine
- prom/memcached-exporter:v0.15.4
- quay.io/prometheus-operator/prometheus-config-reloader:v0.81.0
- quay.io/prometheus-operator/prometheus-operator:v0.88.1
- quay.io/prometheus/node-exporter:v1.10.2
- registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.18.0
Ports / ingress:
- Ingress/grafana: grafana.homelab.local/
- Service/alloy: 12345/TCP -> 12345
- Service/grafana: 80/TCP -> grafana
- Service/loki-canary: 3500/TCP -> http-metrics
- Service/loki-gateway: 80/TCP -> http-metrics
- Service/loki-headless: 3100/TCP -> http-metrics
- Service/loki-memberlist: 7946/TCP -> http-memberlist
- Service/loki-results-cache: 11211/TCP -> client
- Service/loki-results-cache: 9150/TCP -> http-metrics
- Service/loki: 3100/TCP -> http-metrics
- Service/loki: 9095/TCP -> grpc
- Service/prometheus-kube-prometheus-coredns: 9153/TCP -> 9153
- Service/prometheus-kube-prometheus-kube-controller-manager: 10257/TCP -> 10257
- Service/prometheus-kube-prometheus-kube-etcd: 2381/TCP -> 2381
- Service/prometheus-kube-prometheus-kube-proxy: 10249/TCP -> 10249
- Service/prometheus-kube-prometheus-kube-scheduler: 10259/TCP -> 10259
- Service/prometheus-kube-prometheus-operator: 443/TCP -> https
- Service/prometheus-kube-prometheus-prometheus: 8080/TCP -> reloader-web
- Service/prometheus-kube-prometheus-prometheus: 9090/TCP -> 9090
- Service/prometheus-kube-state-metrics: 8080/TCP -> http
- Service/prometheus-operated: 9090/TCP -> http-web
- Service/prometheus-prometheus-node-exporter: 9100/TCP -> 9100
Resources:
- config-reloader: requests={'cpu': '10m', 'memory': '50Mi'}
- grafana: requests={'cpu': '200m', 'memory': '256Mi'}, limits={'cpu': '500m', 'memory': '512Mi'}
- loki: requests={'cpu': '250m', 'memory': '512Mi'}, limits={'cpu': '500m', 'memory': '1Gi'}
- memcached: requests={'cpu': '500m', 'memory': '1229Mi'}, limits={'memory': '1229Mi'}
Dependencies:
- ConfigMap/alloy
- ConfigMap/grafana
- ConfigMap/grafana-dashboards-default
- ConfigMap/loki
- ConfigMap/loki-gateway
- ConfigMap/loki-runtime
- PVC/grafana
- Secret/grafana-admin
- Secret/prometheus-kube-prometheus-admission
- ServiceAccount/alloy
- ServiceAccount/grafana
- ServiceAccount/loki
- ServiceAccount/loki-canary
- ServiceAccount/prometheus-kube-prometheus-admission
- ServiceAccount/prometheus-kube-prometheus-operator
- ServiceAccount/prometheus-kube-state-metrics
- ServiceAccount/prometheus-prometheus-node-exporter
<!-- AUTO-GENERATED:END -->
