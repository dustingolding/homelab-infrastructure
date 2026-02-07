# Homelab Infrastructure

This repository stores Kubernetes manifests and Helm values for the homelab cluster.

Purpose:
- Source of truth for cluster configuration
- Track history and changes via Git
- Enable GitOps workflows (Flux/ArgoCD)

Repository layout:
- `k8s/` — declarative Kubernetes manifests organized by purpose
- `helm/` — Helm charts and values
- `clusters/` — cluster-specific configs
- `scripts/` — helper scripts

See `k8s/README.md` for guidelines on adding manifests.
# homelab-infrastructure
homelab infrastructure automation
