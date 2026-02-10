#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx >/dev/null 2>&1 || true
helm repo update ingress-nginx >/dev/null 2>&1 || true

helm template ingress ingress-nginx/ingress-nginx \
  --version 4.14.3 \
  --namespace ingress-nginx \
  -f namespaces/ingress-nginx/values/ingress.values.yaml \
  > namespaces/ingress-nginx/rendered/ingress-nginx.yaml

helm repo add grafana https://grafana.github.io/helm-charts >/dev/null 2>&1 || true
helm repo update grafana >/dev/null 2>&1 || true

helm template grafana grafana/grafana \
  --version 10.5.15 \
  --namespace monitoring \
  -f namespaces/monitoring/values/grafana.values.yaml \
  > namespaces/monitoring/rendered/grafana.yaml

helm template loki grafana/loki \
  --version 6.51.0 \
  --namespace monitoring \
  -f namespaces/monitoring/values/loki.values.yaml \
  > namespaces/monitoring/rendered/loki.yaml

helm template alloy grafana/alloy \
  --version 1.5.3 \
  --namespace monitoring \
  -f namespaces/monitoring/values/alloy.values.yaml \
  > namespaces/monitoring/rendered/alloy.yaml

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts >/dev/null 2>&1 || true
helm repo update prometheus-community >/dev/null 2>&1 || true

helm template prometheus prometheus-community/kube-prometheus-stack \
  --version 81.5.0 \
  --namespace monitoring \
  -f namespaces/monitoring/values/prometheus.values.yaml \
  > namespaces/monitoring/rendered/prometheus.yaml

helm template mariadb oci://registry-1.docker.io/bitnamicharts/mariadb \
  --version 24.0.4 \
  --namespace cms \
  -f namespaces/cms/values/mariadb.values.yaml \
  > namespaces/cms/rendered/mariadb.yaml

helm template redis oci://registry-1.docker.io/bitnamicharts/redis \
  --version 24.1.3 \
  --namespace cms \
  -f namespaces/cms/values/redis.values.yaml \
  > namespaces/cms/rendered/redis.yaml

helm template wordpress oci://registry-1.docker.io/bitnamicharts/wordpress \
  --version 28.1.5 \
  --namespace cms \
  -f namespaces/cms/values/wordpress.values.yaml \
  > namespaces/cms/rendered/wordpress.yaml
