#!/usr/bin/env bash
set -euo pipefail

# Stream all available Gateway API resources plus only referenced Services.
# Usage:
#   ./get-all-gateway-api.sh > result.yaml

if ! command -v kubectl >/dev/null 2>&1; then
  echo "ERROR: kubectl not found in PATH" >&2
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq not found in PATH" >&2
  exit 1
fi

GROUP="gateway.networking.k8s.io"

# Preferred output order.
preferred=(
  gatewayclasses
  gateways
  httproutes
  grpcroutes
  tcproutes
  tlsroutes
  udproutes
  referencegrants
)

# Detect installed Gateway API resources on this cluster.
# `-o name` may return fully-qualified names like
# `gateways.gateway.networking.k8s.io`, so normalize to base resource names.
mapfile -t available < <(
  kubectl api-resources --api-group="$GROUP" -o name 2>/dev/null \
    | sed "s/\.${GROUP}$//" \
    | sort -u
)

if [ "${#available[@]}" -eq 0 ]; then
  echo "ERROR: No Gateway API resources found in api-group '$GROUP'" >&2
  exit 1
fi

have_kind() {
  local kind="$1"
  local item
  for item in "${available[@]}"; do
    if [ "$item" = "$kind" ]; then
      return 0
    fi
  done
  return 1
}

selected=()
for kind in "${preferred[@]}"; do
  if have_kind "$kind"; then
    selected+=("$kind")
  fi
done

if [ "${#selected[@]}" -eq 0 ]; then
  echo "ERROR: None of the expected Gateway API kinds are installed" >&2
  exit 1
fi

resource_csv=$(IFS=,; echo "${selected[*]}")

# Section 1: Gateway API objects
kubectl get "$resource_csv" -A -o yaml

# Section 2: Referenced Services from route backendRefs
route_kinds=(httproutes grpcroutes tcproutes tlsroutes udproutes)
route_selected=()
for kind in "${route_kinds[@]}"; do
  if have_kind "$kind"; then
    route_selected+=("$kind")
  fi
done

if [ "${#route_selected[@]}" -eq 0 ]; then
  exit 0
fi

route_csv=$(IFS=,; echo "${route_selected[*]}")

svc_refs=$(kubectl get "$route_csv" -A -o json | jq -r '
  .items[] as $r
  | ($r.spec.rules[]?.backendRefs[]? // empty) as $b
  | select(($b.kind // "Service") == "Service")
  | "\($b.namespace // $r.metadata.namespace) \($b.name)"
' | sort -u)

if [ -z "${svc_refs}" ]; then
  exit 0
fi

echo "---"
while read -r ns name; do
  [ -z "${ns:-}" ] && continue
  kubectl -n "$ns" get svc "$name" -o yaml || true
  echo "---"
done <<< "$svc_refs"
