#!/usr/bin/env bash
set -euo pipefail

NS="recipelab"
TMP_POD="recipelab-smoke"

kubectl -n "$NS" rollout status deployment/recipelab-api
kubectl -n "$NS" rollout status deployment/recipelab-web
kubectl -n "$NS" rollout status deployment/recipelab-worker
kubectl -n "$NS" rollout status deployment/recipelab-redis
kubectl -n "$NS" rollout status statefulset/recipelab-postgres

kubectl -n "$NS" delete pod "$TMP_POD" --ignore-not-found
kubectl -n "$NS" run "$TMP_POD" --image=curlimages/curl:8.7.1 --restart=Never --command -- sleep 3600
kubectl -n "$NS" wait --for=condition=Ready pod/$TMP_POD --timeout=120s

kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS http://recipelab-api.$NS.svc.cluster.local:8000/healthz
kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS http://recipelab-api.$NS.svc.cluster.local:8000/readyz

kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS -X POST \
  -F "content=1 cup flour\n2 eggs\nBake at 350F for 20m" \
  -F "title=Test Muffins" \
  http://recipelab-api.$NS.svc.cluster.local:8000/recipes/import

kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS \
  "http://recipelab-api.$NS.svc.cluster.local:8000/recipes/search?q=muffins"

OPENAI_KEY=$(kubectl -n "$NS" get secret recipelab-secrets -o jsonpath='{.data.OPENAI_API_KEY}' 2>/dev/null || true)
if [[ -n "$OPENAI_KEY" ]]; then
  kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS -X POST \
    -F "message=What substitutions can I make for eggs?" \
    -F "layers=pantry" \
    http://recipelab-api.$NS.svc.cluster.local:8000/chat
else
  echo "Skipping chat test: OPENAI_API_KEY secret not found in cluster."
fi

INGRESS_IP=$(kubectl -n "$NS" get ingress recipelab -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null || true)
if [[ -n "$INGRESS_IP" ]]; then
  kubectl -n "$NS" exec "$TMP_POD" -- curl -fsS -H "Host: recipelab.homelab.local" "http://$INGRESS_IP/"
else
  echo "Ingress has no load balancer IP yet."
fi

kubectl -n "$NS" delete pod "$TMP_POD" --ignore-not-found
