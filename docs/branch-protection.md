# Branch Protection (Recommended)

This repo assumes strict branch protection on `main`.

## Baseline (Solo)
- Require pull request reviews before merging: On
- Required approvals: 1
- Dismiss stale approvals when new commits are pushed: On
- Require conversation resolution: On
- Require status checks to pass before merging: On
- Require branches to be up to date before merging: On
- Include administrators: On
- Restrict who can push: On (only you + automation)

## Optional (Decide Later)
- Require signed commits: Optional
- Require linear history: Optional
- Require code owners: On (if `CODEOWNERS` exists)

## Required Status Checks
- `validate-docs / namespace-docs`
- `validate-live-cluster / live-cluster-diff`

## Notes
- `validate-live-cluster` requires a self-hosted runner with cluster access.
- If the live check is unavailable, you can temporarily disable it to unblock merges, but re-enable immediately after.
