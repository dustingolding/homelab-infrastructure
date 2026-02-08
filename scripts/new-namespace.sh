#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NS="${1:-}"

if [[ -z "$NS" ]]; then
  echo "Usage: $0 <namespace>" >&2
  exit 2
fi

NS_DIR="$ROOT/namespaces/$NS"

if [[ -d "$NS_DIR" ]]; then
  echo "ERROR: namespace already exists: $NS_DIR" >&2
  exit 1
fi

mkdir -p "$NS_DIR"/{apps,backups,network,rbac,storage,values}

cat > "$NS_DIR/README.md" <<EOF2
# ${NS} Namespace

## Overview (Manual)
Describe why this namespace exists.

## Access (Manual)
Describe how to access services here.

---

## 🔁 Generated Section (DO NOT EDIT BELOW)

<!-- AUTO-GENERATED:START -->
Deployed services:
- placeholder
Images & versions:
- placeholder
Ports / ingress:
- placeholder
Resources:
- placeholder
Dependencies:
- placeholder
<!-- AUTO-GENERATED:END -->
EOF2

cat > "$NS_DIR/namespace.meta.yaml" <<EOF2
name: ${NS}
purpose: Describe why this namespace exists.
access: Describe how to access services here.
upgrade: Describe how to upgrade services safely.
destroy: Describe how to destroy services safely.
owners:
  - dustin
EOF2

touch "$NS_DIR"/apps/.keep "$NS_DIR"/backups/.keep "$NS_DIR"/network/.keep \
  "$NS_DIR"/rbac/.keep "$NS_DIR"/storage/.keep "$NS_DIR"/values/.keep

echo "Created namespace: $NS_DIR"
