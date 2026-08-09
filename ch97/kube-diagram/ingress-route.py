#!/usr/bin/env python3

import argparse
import sys
from typing import Any, Dict, List, Optional

import yaml


def parse_destination(destination: str) -> Dict[str, Any]:
    host_and_port = destination.strip()
    if ":" in host_and_port:
        host, port_str = host_and_port.rsplit(":", 1)
        try:
            port = int(port_str)
        except ValueError:
            port = None
    else:
        host = host_and_port
        port = None

    parts = host.split(".")
    name = parts[0] if parts else host
    namespace: Optional[str] = None

    if len(parts) >= 2 and parts[1] != "svc":
        namespace = parts[1]

    backend: Dict[str, Any] = {
        "kind": "Service",
        "name": name,
    }
    if namespace:
        backend["namespace"] = namespace
    if port is not None:
        backend["port"] = port

    return backend


def path_type_to_httproute(path_type: Optional[str]) -> str:
    mapping = {
        "Prefix": "PathPrefix",
        "Exact": "Exact",
        "ImplementationSpecific": "RegularExpression",
    }
    return mapping.get(path_type or "", "PathPrefix")


def build_backend_ref(path_entry: Dict[str, Any], ingress: Dict[str, Any]) -> Dict[str, Any]:
    annotations = ingress.get("metadata", {}).get("annotations", {})
    destination = annotations.get("higress.io/destination")
    if destination:
        return parse_destination(destination)

    backend = path_entry.get("backend", {})
    service = backend.get("service")
    if service:
        result = {
            "kind": "Service",
            "name": service.get("name"),
        }
        port_info = service.get("port", {})
        if "number" in port_info:
            result["port"] = port_info["number"]
        elif "name" in port_info:
            result["port"] = port_info["name"]
        return result

    resource = backend.get("resource")
    if resource:
        result = {
            "group": resource.get("apiGroup"),
            "kind": resource.get("kind"),
            "name": resource.get("name"),
        }
        return {k: v for k, v in result.items() if v is not None}

    return {
        "kind": "Service",
        "name": "unknown-backend",
    }


def ingress_to_httproutes(
    ingress: Dict[str, Any],
    gateway_name: str,
    gateway_namespace: str,
    route_name_suffix: str,
) -> Optional[Dict[str, Any]]:
    if ingress.get("kind") != "Ingress":
        return None

    metadata = ingress.get("metadata", {})
    spec = ingress.get("spec", {})
    ingress_namespace = metadata.get("namespace", "default")
    rules = spec.get("rules", [])

    route_name = f"{metadata.get('name', 'ingress')}{route_name_suffix}"
    result: Dict[str, Any] = {
        "apiVersion": "gateway.networking.k8s.io/v1",
        "kind": "HTTPRoute",
        "metadata": {
            "name": route_name,
            "namespace": ingress_namespace,
        },
        "spec": {
            "parentRefs": [
                {
                    "group": "gateway.networking.k8s.io",
                    "kind": "Gateway",
                    "name": gateway_name,
                    "namespace": gateway_namespace,
                }
            ],
            "rules": [],
        },
    }

    hostnames: List[str] = []
    route_namespace = ingress_namespace
    for rule in rules:
        host = rule.get("host")
        if host:
            hostnames.append(host)

        for path_entry in rule.get("http", {}).get("paths", []):
            match = {
                "path": {
                    "type": path_type_to_httproute(path_entry.get("pathType")),
                    "value": path_entry.get("path", "/"),
                }
            }
            backend_ref = build_backend_ref(path_entry, ingress)
            backend_namespace = backend_ref.get("namespace")
            if backend_namespace:
                route_namespace = backend_namespace

            result["spec"]["rules"].append(
                {
                    "matches": [match],
                    "backendRefs": [backend_ref],
                }
            )

    if hostnames:
        result["spec"]["hostnames"] = hostnames

    result["metadata"]["namespace"] = route_namespace

    return result


def iter_ingresses(doc: Any) -> List[Dict[str, Any]]:
    if not isinstance(doc, dict):
        return []
    if doc.get("kind") == "Ingress":
        return [doc]
    if isinstance(doc.get("items"), list):
        return [item for item in doc["items"] if isinstance(item, dict) and item.get("kind") == "Ingress"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Kubernetes Ingress resources to HTTPRoute resources")
    parser.add_argument("input", help="Input YAML file containing Ingress or List")
    parser.add_argument("-o", "--output", help="Output YAML file (default: stdout)")
    parser.add_argument("--gateway-name", default="higress-gateway", help="Gateway name for parentRefs")
    parser.add_argument("--gateway-namespace", default="higress-system", help="Gateway namespace for parentRefs")
    parser.add_argument("--route-name-suffix", default="", help="Suffix to append to generated HTTPRoute name")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as handle:
        docs = list(yaml.safe_load_all(handle))

    routes: List[Dict[str, Any]] = []
    for doc in docs:
        for ingress in iter_ingresses(doc):
            route = ingress_to_httproutes(
                ingress,
                gateway_name=args.gateway_name,
                gateway_namespace=args.gateway_namespace,
                route_name_suffix=args.route_name_suffix,
            )
            if route:
                routes.append(route)

    if not routes:
        print("No Ingress resources found.", file=sys.stderr)
        return 1

    output = yaml.safe_dump_all(routes, sort_keys=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
