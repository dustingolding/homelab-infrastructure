# RecipeLab Conventions

## Deployment Pattern Summary
- GitOps via Flux with Kustomize: `clusters/k3s-homelab/flux-system/gotk-sync.yaml` and `clusters/k3s-homelab/kustomization.yaml` reference `cluster-scope/` and `namespaces/` directly.
- Namespace-first structure: `namespaces/README.md` defines one folder per namespace with grouped subfolders (apps, network, storage, etc.).
- Namespace metadata is required: `docs/namespace-meta.schema.yaml` and `namespaces/*/namespace.meta.yaml`.
- Cluster-wide resources live in `cluster-scope/` (including Namespace objects in `cluster-scope/namespace/`).

## Discovered Standards (with evidence)
- Ingress classes in use (nginx): `ingressClassName: nginx` in `namespaces/cms/network/wordpress.ingress.yaml`.
- Ingress classes in use (traefik): `ingressClassName: traefik` plus `traefik.ingress.kubernetes.io/router.entrypoints: web` in `namespaces/monitoring/network/grafana.ingress.yaml`.
- IngressClass definitions live in `cluster-scope/ingressclasses/nginx.ingressclass.yaml` and `cluster-scope/ingressclasses/traefik.ingressclass.yaml`.
- Namespaces are defined in `cluster-scope/namespace/*.namespace.yaml` with the `kubernetes.io/metadata.name` label (example: `cluster-scope/namespace/cms.namespace.yaml`).
- Per-namespace files are grouped by purpose (example: `namespaces/cms/apps`, `namespaces/cms/network`, `namespaces/cms/storage`).
- Secrets are managed with SOPS + age per `docs/secrets.md` and `.sops.yaml`.
- Default storage class is `local-path` per `cluster-scope/storage/local-path.storageclass.yaml`.
- PVCs reference `local-path` in `namespaces/cms/storage/cms-backups-pvc.persistentvolumeclaim.yaml`.
- Logs are shipped by Alloy which discovers all pods via `namespaces/observability/apps/alloy-config.configmap.yaml`.
- Prometheus is installed via Helm values in `namespaces/monitoring/values/prometheus.values.yaml`.
- No ServiceMonitor/PodMonitor resources appear in namespaces (only CRDs exist in `cluster-scope/crds/`).
- Existing manifests use minimal labels in `namespaces/cms/apps/*.yaml` and `namespaces/cms/network/wordpress.ingress.yaml`.
- Existing workloads use public images in `namespaces/*/apps/*.yaml` and values files.

## RecipeLab Alignment
- RecipeLab uses `ingressClassName: traefik` and the `homelab.local` internal DNS pattern to mirror the Grafana ingress pattern.
- RecipeLab stores secrets in a SOPS-encrypted secret manifest and uses `local-path` PVCs for Postgres, matching existing storage conventions.
