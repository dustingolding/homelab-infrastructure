#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT/scripts/export-helm-values.py"
python3 "$ROOT/scripts/gen-namespace-docs.py"

git -C "$ROOT" diff --exit-code
