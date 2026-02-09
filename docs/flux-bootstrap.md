# Flux Bootstrap

This repo uses Flux for GitOps.

## Install Flux CLI
```bash
curl -s https://fluxcd.io/install.sh | sudo bash
```

## Bootstrap (GitHub)
```bash
flux bootstrap github \
  --owner=dustingolding \
  --repo=homelab-infrastructure \
  --branch=main \
  --path=./clusters/k3s-homelab \
  --personal
```

## Verify
```bash
flux check
flux get kustomizations -A
```
