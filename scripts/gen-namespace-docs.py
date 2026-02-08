#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

try:
    import yaml
except Exception:
    print("ERROR: PyYAML is required. Install with: pip3 install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
NAMESPACES_DIR = ROOT / "namespaces"
META_FILE = "namespace.meta.yaml"

START = "<!-- AUTO-GENERATED:START -->"
END = "<!-- AUTO-GENERATED:END -->"

WORKLOAD_KINDS = {
    "Deployment",
    "StatefulSet",
    "DaemonSet",
    "Job",
    "CronJob",
    "ReplicaSet",
}
SERVICE_KINDS = {
    "Service",
    "Ingress",
}


def iter_yaml_docs(path):
    with path.open("r", encoding="utf-8") as f:
        try:
            for doc in yaml.safe_load_all(f):
                if isinstance(doc, dict):
                    yield doc
        except yaml.YAMLError:
            return


def collect_pod_specs(obj):
    kind = obj.get("kind")
    spec = obj.get("spec") or {}
    pod_specs = []
    if kind == "CronJob":
        pod_specs.append(
            (((spec.get("jobTemplate") or {}).get("spec") or {}).get("template") or {}).get("spec")
        )
    elif kind in {"Job"}:
        pod_specs.append(((spec.get("template") or {}).get("spec") or {}))
    elif kind in {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet"}:
        pod_specs.append(((spec.get("template") or {}).get("spec") or {}))
    return [p for p in pod_specs if isinstance(p, dict)]


def extract_images_from_values(obj):
    images = set()

    def walk(value, parent=None, key=None):
        if isinstance(value, dict):
            repo = value.get("repository")
            tag = value.get("tag")
            image = value.get("image")
            if isinstance(image, str) and image:
                images.add(image)
            if key in {"image", "images"} and isinstance(value, str) and value:
                images.add(value)
            if isinstance(repo, str) and repo:
                if isinstance(tag, str) and tag:
                    images.add(f"{repo}:{tag}")
                else:
                    images.add(repo)
            for k, v in value.items():
                walk(v, parent=value, key=k)
        elif isinstance(value, list):
            for v in value:
                walk(v, parent=parent, key=key)
        elif isinstance(value, str):
            if key in {"image", "images"} and value:
                images.add(value)

    walk(obj)
    return images


def read_meta(ns_dir):
    meta_path = ns_dir / META_FILE
    if not meta_path.exists():
        print(f"ERROR: missing {META_FILE} in {ns_dir}", file=sys.stderr)
        return None
    try:
        data = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        print(f"ERROR: invalid YAML in {meta_path}", file=sys.stderr)
        return None
    return data


def extract_namespace_entries(ns_dir):
    services = set()
    images = set()
    helm_images = set()
    ports = set()
    resources = set()
    deps = set()
    values_files = set()

    for path in ns_dir.rglob("*.yaml"):
        if path.parent.name == "values":
            values_files.add(str(path.relative_to(ns_dir)))
            for doc in iter_yaml_docs(path):
                if isinstance(doc, dict):
                    helm_images.update(extract_images_from_values(doc))
        for doc in iter_yaml_docs(path):
            if "apiVersion" not in doc or "kind" not in doc:
                continue
            kind = doc.get("kind")
            metadata = doc.get("metadata") or {}
            name = metadata.get("name")
            if name and (kind in WORKLOAD_KINDS or kind in SERVICE_KINDS):
                services.add(f"{kind}/{name}")

            if kind == "Service":
                for p in (doc.get("spec") or {}).get("ports") or []:
                    port = p.get("port")
                    protocol = p.get("protocol", "TCP")
                    target = p.get("targetPort")
                    if port:
                        if target:
                            ports.add(f"Service/{name}: {port}/{protocol} -> {target}")
                        else:
                            ports.add(f"Service/{name}: {port}/{protocol}")

            if kind == "Ingress":
                rules = (doc.get("spec") or {}).get("rules") or []
                for r in rules:
                    host = r.get("host")
                    http = r.get("http") or {}
                    paths = http.get("paths") or []
                    if host:
                        if paths:
                            for p in paths:
                                pathv = p.get("path", "/")
                                ports.add(f"Ingress/{name}: {host}{pathv}")
                        else:
                            ports.add(f"Ingress/{name}: {host}")

            for pod_spec in collect_pod_specs(doc):
                sa = pod_spec.get("serviceAccountName")
                if sa:
                    deps.add(f"ServiceAccount/{sa}")

                for v in pod_spec.get("volumes") or []:
                    if "persistentVolumeClaim" in v:
                        pvc = (v.get("persistentVolumeClaim") or {}).get("claimName")
                        if pvc:
                            deps.add(f"PVC/{pvc}")
                    if "secret" in v:
                        sec = (v.get("secret") or {}).get("secretName")
                        if sec:
                            deps.add(f"Secret/{sec}")
                    if "configMap" in v:
                        cm = (v.get("configMap") or {}).get("name")
                        if cm:
                            deps.add(f"ConfigMap/{cm}")

                for c in (pod_spec.get("initContainers") or []) + (pod_spec.get("containers") or []):
                    img = c.get("image")
                    if img:
                        images.add(img)
                    res = c.get("resources") or {}
                    req = res.get("requests")
                    lim = res.get("limits")
                    if req or lim:
                        parts = []
                        if req:
                            parts.append(f"requests={req}")
                        if lim:
                            parts.append(f"limits={lim}")
                        cname = c.get("name", "container")
                        resources.add(f"{cname}: " + ", ".join(parts))

                    for envfrom in c.get("envFrom") or []:
                        if "secretRef" in envfrom:
                            sec = (envfrom.get("secretRef") or {}).get("name")
                            if sec:
                                deps.add(f"Secret/{sec}")
                        if "configMapRef" in envfrom:
                            cm = (envfrom.get("configMapRef") or {}).get("name")
                            if cm:
                                deps.add(f"ConfigMap/{cm}")

                    for env in c.get("env") or []:
                        vf = env.get("valueFrom") or {}
                        if "secretKeyRef" in vf:
                            sec = (vf.get("secretKeyRef") or {}).get("name")
                            if sec:
                                deps.add(f"Secret/{sec}")
                        if "configMapKeyRef" in vf:
                            cm = (vf.get("configMapKeyRef") or {}).get("name")
                            if cm:
                                deps.add(f"ConfigMap/{cm}")

    def as_list(items):
        return sorted(items) if items else ["none"]

    return {
        "services": as_list(services),
        "images": as_list(images),
        "helm_images": as_list(helm_images),
        "ports": as_list(ports),
        "resources": as_list(resources),
        "deps": as_list(deps),
        "values": as_list(values_files),
    }


def update_readme(ns_dir, check_only=False):
    readme = ns_dir / "README.md"
    if not readme.exists():
        print(f"ERROR: missing README.md in {ns_dir}", file=sys.stderr)
        return False

    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"ERROR: missing markers in {readme}", file=sys.stderr)
        return False

    start_idx = text.index(START) + len(START)
    end_idx = text.index(END)

    meta = read_meta(ns_dir)
    if meta is None:
        return False

    data = extract_namespace_entries(ns_dir)
    owners = meta.get("owners") or []
    owners_value = ", ".join(owners) if owners else "none"
    exposure = meta.get("exposure") or {}
    meta_data = meta.get("data") or {}
    deps = meta.get("dependencies") or []
    domains = exposure.get("domains") or []
    components = meta_data.get("components") or []
    purpose = str(meta.get("purpose", "unknown")).replace("\n", " ").strip()

    def fmt_bool(value):
        if isinstance(value, bool):
            return "true" if value else "false"
        return value if value is not None else "unknown"
    gen = "\n".join([
        "",
        "Metadata:",
        f"- namespace: {meta.get('namespace', 'unknown')}",
        f"- purpose: {purpose or 'unknown'}",
        f"- exposure.type: {exposure.get('type', 'unknown')}",
        f"- exposure.ingress: {exposure.get('ingress', 'unknown')}",
        f"- exposure.domains: {', '.join(domains) if domains else 'none'}",
        f"- data.persistence: {fmt_bool(meta_data.get('persistence'))}",
        f"- data.components: {', '.join(components) if components else 'none'}",
        f"- data.backup_required: {fmt_bool(meta_data.get('backup_required'))}",
        f"- dependencies: {', '.join(deps) if deps else 'none'}",
        f"- criticality: {meta.get('criticality', 'unknown')}",
        f"- rebuild_time_estimate: {meta.get('rebuild_time_estimate', 'unknown')}",
        f"- owners: {owners_value}",
        "Deployed services:",
        *[f"- {s}" for s in data["services"]],
        "Helm values:",
        *[f"- {s}" for s in data["values"]],
        "Helm images (values):",
        *[f"- {s}" for s in data["helm_images"]],
        "Images & versions:",
        *[f"- {s}" for s in data["images"]],
        "Ports / ingress:",
        *[f"- {s}" for s in data["ports"]],
        "Resources:",
        *[f"- {s}" for s in data["resources"]],
        "Dependencies:",
        *[f"- {s}" for s in data["deps"]],
        "",
    ])

    new_text = text[:start_idx] + gen + text[end_idx:]
    if check_only:
        if new_text != text:
            print(f"ERROR: stale README: {readme}", file=sys.stderr)
            return False
        return True
    readme.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if docs are stale")
    args = parser.parse_args()

    if not NAMESPACES_DIR.exists():
        print("ERROR: namespaces/ not found", file=sys.stderr)
        sys.exit(2)

    ok = True
    for ns_dir in sorted(p for p in NAMESPACES_DIR.iterdir() if p.is_dir()):
        if ns_dir.name.startswith("."):
            continue
        if not update_readme(ns_dir, check_only=args.check):
            ok = False

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
