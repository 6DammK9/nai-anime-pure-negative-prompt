#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
FILL_REFERENCES_SCRIPT="${FILL_REFERENCES_SCRIPT:-$SCRIPT_DIR/fill-references-stubonly.sh}"
KUBEDIAGRAMS_IMAGE="${KUBEDIAGRAMS_IMAGE:-philippemerle/kubediagrams}"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "Error: kubectl is not installed or not in PATH" >&2
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: docker is not installed or not in PATH" >&2
  exit 1
fi

if [[ ! -x "$FILL_REFERENCES_SCRIPT" ]]; then
  echo "Error: fill_references script not executable: $FILL_REFERENCES_SCRIPT" >&2
  exit 1
fi

namespaces=$(kubectl get ns -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}')

if [[ -z "$namespaces" ]]; then
  echo "No namespaces found." >&2
  exit 0
fi

while IFS= read -r namespace; do
  [[ -z "$namespace" ]] && continue
  echo "Generating ${namespace}.svg"

  if [[ "$namespace" == "kube-system" ]]; then
    kubectl get all -n "$namespace" -o yaml \
      | "$FILL_REFERENCES_SCRIPT" \
      | docker run --rm -v "$(pwd)":/work -i "$KUBEDIAGRAMS_IMAGE" \
        kube-diagrams -f svg --embed-all-icons -o "/work/${namespace}.svg" -
  else
    kubectl get-all -n "$namespace" -o yaml \
      | "$FILL_REFERENCES_SCRIPT" \
      | docker run --rm -v "$(pwd)":/work -i "$KUBEDIAGRAMS_IMAGE" \
        kube-diagrams -f svg --embed-all-icons -o "/work/${namespace}.svg" -
  fi
done <<< "$namespaces"

echo "Done. Generated SVG files per namespace in: $(pwd)"
