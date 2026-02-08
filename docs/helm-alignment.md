# Helm Alignment

This repo can align values and chart pins with the live cluster.

## Export Values + Pins
```bash
python3 scripts/export-helm-values.py
```

## Verify Live Cluster Matches Repo
```bash
scripts/verify-live-cluster.sh
```

This will fail if exported values or generated docs drift from what is in Git.
