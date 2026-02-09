# RecipeLab Observability

## Logging
- Logs are collected by Alloy from all pods in the cluster.
- No additional pod annotations are required based on current observability patterns.

## Metrics
- API exposes Prometheus metrics at `/metrics`.
- Prometheus is already deployed in the `monitoring` namespace.
- No ServiceMonitor resources are currently used in namespaces.

## Suggested Dashboards
- API request volume and error rate.
- OpenAI latency and error rates (add custom metrics if needed).
- Worker job failures and job backlog (add custom metrics if needed).
- Postgres connection health (via `/readyz`).
