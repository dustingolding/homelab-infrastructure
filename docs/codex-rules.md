# Codex Rules

These rules are authoritative for repo automation.

## README Generation
- Only edit content between `<!-- AUTO-GENERATED:START -->` and `<!-- AUTO-GENERATED:END -->`.
- Never touch manual sections.
- Fail if markers are missing.
- Generated content is derived from `namespace.meta.yaml`, manifests, and Helm values.

## Metadata
- Every namespace must include `namespace.meta.yaml`.
- Schema reference: `docs/namespace-meta.schema.yaml`.

## Change Management
- All changes are made via Git commits.
- No manual edits to live clusters without a matching commit.
- Every change must be reviewable, reversible, and explainable.
- `main` is protected and requires passing checks and review.

## Helm Values Export
- Use `scripts/export-helm-values.py` to align repo values with live Helm releases.
- Secrets and sensitive fields are redacted during export.
- Per-namespace chart pins are written to `namespaces/<namespace>/charts.yaml`.
