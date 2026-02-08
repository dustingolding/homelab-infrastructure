# Checklist
- [ ] I ran `python3 scripts/gen-namespace-docs.py` (or CI did) and docs are up to date.
- [ ] I ran `python3 scripts/export-helm-values.py` if Helm values changed.
- [ ] I ran `scripts/verify-live-cluster.sh` if this change should match the live cluster.
- [ ] I updated `namespace.meta.yaml` and manual README sections as needed.

# Summary
Describe what changed and why.

# Risk
What could break? How to rollback?

# Notes
Anything else reviewers should know.
