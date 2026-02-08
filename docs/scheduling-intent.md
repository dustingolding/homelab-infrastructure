# Scheduling Intent

## Node Labels (Required)
Run once to label nodes:

```bash
# Proxmox workers
kubectl label node k3s-w1 node.type=vm node.platform=amd64
kubectl label node k3s-w2 node.type=vm node.platform=amd64

# Raspberry Pi
kubectl label node k3s-w3 node.type=pi node.platform=arm64

# Bare metal
kubectl label node k3s-baremetal-w4 node.type=baremetal node.platform=amd64
```

Verify:
```bash
kubectl get nodes --show-labels
```

## Scheduling Intent (Document First)

CMS (WordPress / MariaDB / Redis):
- Run on Proxmox VMs or bare metal.
- Do NOT run on Raspberry Pi by default.
- Use node selectors (not taints) for now.

Monitoring (Prometheus / Grafana / Loki):
- Run on Proxmox VMs or bare metal.
- Pi allowed only for log shippers.

Observability (Alloy):
- Run on every node (DaemonSet).

## Optional (Later)
Gentle enforcement via selectors/affinity once intent is documented:

```yaml
nodeSelector:
  node.platform: amd64
```

```yaml
affinity:
  nodeAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        preference:
          matchExpressions:
            - key: node.type
              operator: In
              values: ["baremetal"]
```
