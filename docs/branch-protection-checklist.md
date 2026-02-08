# Branch Protection Checklist (homelab-infrastructure)

Apply to branch pattern: `main`

## Required
- Require a pull request before merging
- Required approvals: 1
- Dismiss stale approvals when new commits are pushed
- Require conversation resolution
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Include administrators
- Restrict who can push (only you + automation)

## Required Status Checks
- `validate-docs / namespace-docs`
- `validate-live-cluster / live-cluster-diff`

## Optional
- Require signed commits
- Require linear history
- Require review from Code Owners
