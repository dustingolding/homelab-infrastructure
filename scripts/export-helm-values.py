#!/usr/bin/env python3
import subprocess
import yaml
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REDACTION_CONFIG = ROOT / "scripts" / "redaction.yaml"

RELEASES = [
    ("cms", "wordpress", "cms"),
    ("cms", "mariadb", "cms"),
    ("cms", "redis", "cms"),
    ("ingress-nginx", "ingress", "ingress-nginx"),
    ("monitoring", "grafana", "monitoring"),
    ("monitoring", "loki", "monitoring"),
    ("monitoring", "prometheus", "monitoring"),
    ("monitoring", "alloy", "monitoring"),
]

DEFAULT_DENY = [
    r"password",
    r"passwd",
    r"token",
    r"api[_-]?key",
    r"access[_-]?key",
    r"private[_-]?key",
    r"client[_-]?secret",
]
DEFAULT_ALLOW = [
    "allowEmptyPassword",
    "existingSecret",
    "secretName",
    "secretRef",
    "secretKeyRef",
    "secret",
]


def load_redaction():
    allow = set(k.lower() for k in DEFAULT_ALLOW)
    deny = list(DEFAULT_DENY)
    if REDACTION_CONFIG.exists():
        cfg = yaml.safe_load(REDACTION_CONFIG.read_text(encoding="utf-8")) or {}
        for k in cfg.get("allow_keys") or []:
            allow.add(str(k).lower())
        for p in cfg.get("deny_patterns") or []:
            deny.append(str(p))
    return allow, re.compile("|".join(deny), re.I)


ALLOW_KEYS, SENSITIVE_MATCH = load_redaction()


def is_sensitive_key(key):
    if not isinstance(key, str):
        return False
    kl = key.lower()
    if kl in ALLOW_KEYS:
        return False
    return bool(SENSITIVE_MATCH.search(kl))


def sanitize(obj, key=None):
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if is_sensitive_key(k):
                if isinstance(v, (str, int, float)):
                    new[k] = "<<REDACTED>>"
                else:
                    new[k] = sanitize(v, key=k)
            else:
                new[k] = sanitize(v, key=k)
        return new
    if isinstance(obj, list):
        return [sanitize(v, key=key) for v in obj]
    return obj


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def export_values():
    for ns, rel, ns_folder in RELEASES:
        out = run(["helm", "-n", ns, "get", "values", rel, "-o", "yaml"])
        if out.returncode != 0:
            print(f"skip {ns}/{rel}: {out.stderr.strip()}")
            continue
        data = yaml.safe_load(out.stdout) or {}
        if isinstance(data, dict) and "USER-SUPPLIED VALUES" in data:
            data.pop("USER-SUPPLIED VALUES", None)
        data = sanitize(data)
        out_path = ROOT / "namespaces" / ns_folder / "values" / f"{rel}.values.yaml"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        print(f"wrote {out_path}")


def export_pins():
    out = run(["helm", "list", "-A", "-o", "json"])
    if out.returncode != 0:
        print(out.stderr.strip())
        return
    try:
        items = json.loads(out.stdout)
    except Exception:
        print("ERROR: failed to parse helm list JSON")
        return
    pins = []
    per_namespace = {}
    for it in items:
        name = it.get("name")
        namespace = it.get("namespace")
        chart = it.get("chart")
        appv = it.get("app_version")
        if name and namespace and chart:
            entry = {"release": name, "namespace": namespace, "chart": chart, "appVersion": appv}
            pins.append(entry)
            per_namespace.setdefault(namespace, []).append(entry)
    pin_path = ROOT / "docs" / "helm-releases.yaml"
    pin_path.write_text(yaml.safe_dump(pins, sort_keys=False), encoding="utf-8")
    print(f"wrote {pin_path}")

    # Write per-namespace chart pins
    for ns, entries in per_namespace.items():
        ns_dir = ROOT / "namespaces" / ns
        if not ns_dir.exists():
            continue
        chart_path = ns_dir / "charts.yaml"
        chart_path.write_text(yaml.safe_dump(entries, sort_keys=False), encoding="utf-8")
        print(f"wrote {chart_path}")


def main():
    export_values()
    export_pins()


if __name__ == "__main__":
    main()
