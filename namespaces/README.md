# Namespaces

This repo treats namespaces as first-class units. Each namespace gets its own folder that contains the resources scoped to that namespace.

Conventions:
- One folder per namespace under `namespaces/`.
- Keep resources grouped by purpose (for example: `apps/`, `backups/`, `rbac/`, `network/`, `storage/`, `values/`).
- Cluster-specific overrides live under `clusters/<cluster>/namespaces/<namespace>/`.

Documentation:
- Every namespace README uses manual sections plus an auto-generated section.
- Codex must only edit content between the markers and fail if markers are missing.
- Every namespace must include `namespace.meta.yaml`.

Example:
- `namespaces/cms/`
- `clusters/k3s-homelab/namespaces/cms/`
