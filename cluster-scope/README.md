# Cluster-Scope

Cluster-wide resources that are not namespace-scoped.

Contents:
- `crds/` — CustomResourceDefinitions
- `rbac/` — ClusterRoles and ClusterRoleBindings
- `storage/` — StorageClasses
- `priority/` — PriorityClasses
- `ingressclasses/` — IngressClasses
- `admission/` — Mutating/Validating webhooks
- `namespace/` — Namespace objects

Refresh:
```bash
kubectl get crd -o yaml > cluster-scope/crds/crds.yaml
kubectl get clusterrole -o yaml > cluster-scope/rbac/clusterroles.yaml
kubectl get clusterrolebinding -o yaml > cluster-scope/rbac/clusterrolebindings.yaml
kubectl get storageclass -o yaml > cluster-scope/storage/storageclasses.yaml
kubectl get priorityclass -o yaml > cluster-scope/priority/priorityclasses.yaml
kubectl get ingressclass -o yaml > cluster-scope/ingressclasses/ingressclasses.yaml
kubectl get mutatingwebhookconfiguration -o yaml > cluster-scope/admission/mutatingwebhooks.yaml
kubectl get validatingwebhookconfiguration -o yaml > cluster-scope/admission/validatingwebhooks.yaml
kubectl get namespace -o yaml > cluster-scope/namespace/namespaces.yaml
```
