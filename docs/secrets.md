# Secrets Management (SOPS + age)

We do not store plaintext secrets in Git. Use SOPS with age.

## Setup
1. Install tools:
   - sops
   - age
2. Generate an age key:
```bash
age-keygen -o ~/.config/sops/age/keys.txt
```
3. Export the public key to `.sops.yaml` (replace `AGE_PUBLIC_KEY_HERE`).

## Encrypt a secret
Create a secret file as `*.sops.yaml` and encrypt:
```bash
sops --encrypt --in-place namespaces/cms/secrets/wordpress-db.sops.yaml
```

## Decrypt (for kubectl apply)
```bash
sops --decrypt namespaces/cms/secrets/wordpress-db.sops.yaml | kubectl apply -f -
```

## Notes
- Only `data` and `stringData` are encrypted.
- Keep `age` private key off the cluster.
