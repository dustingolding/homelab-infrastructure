# Kubernetes Manifests

Place Kubernetes manifests here, organized by purpose (namespaces, apps, backups, rbac, etc.).

Guidelines:
- Keep manifests small and modular.
- Prefer one resource per file when practical.
- Use `kustomize` or Helm for templating; store generated manifests in a separate directory if needed.
- Don't store secrets in plaintext; use sealed-secrets, SOPS, or external secret controllers.
