# RecipeLab Security

## Secrets
- All secrets are stored in SOPS-encrypted manifests.
- No plaintext secrets are committed.

## OpenAI Usage
- OpenAI API keys are only used by the backend services.
- No direct browser-side OpenAI calls.

## Network
- Only the web UI is exposed via ingress.
- API is routed through the ingress under `/api`.
- Postgres and Redis remain cluster-internal.

## Access
- The current UI uses local-only username storage as a placeholder.
- For stronger auth, add SSO or reverse-proxy auth consistent with cluster standards.

## Data Handling
- Stored recipes and preferences are internal to the cluster.
- Ensure backups are secured and access-controlled.
