#!/usr/bin/env bash
set -euo pipefail

KUBEDIAGRAMS_IMAGE="${KUBEDIAGRAMS_IMAGE:-philippemerle/kubediagrams}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but not found in PATH" >&2
  exit 1
fi

tmp_input_noeps="$(mktemp)"
tmp_input="$(mktemp)"
tmp_log="$(mktemp)"
tmp_probe_png="$(mktemp --suffix=.png)"
trap 'rm -f "$tmp_input_noeps" "$tmp_input" "$tmp_log" "$tmp_probe_png"' EXIT

cat > "$tmp_input"

if [[ ! -s "$tmp_input" ]]; then
  echo "stdin is empty; provide Kubernetes YAML via pipe" >&2
  exit 1
fi

# Drop EndpointSlice docs to avoid kube-diagrams KeyError on Node targetRef without namespace.
awk '
function flush_doc() {
  if (doc_len == 0) {
    return
  }
  if (!doc_is_endpointslice) {
    for (i = 1; i <= doc_len; i++) {
      print doc[i]
    }
  }
  delete doc
  doc_len = 0
  doc_is_endpointslice = 0
}

/^---[[:space:]]*$/ {
  flush_doc()
  doc_len = 1
  doc[doc_len] = $0
  next
}

{
  if (doc_len == 0) {
    doc_len = 1
    doc[doc_len] = $0
  } else {
    doc[++doc_len] = $0
  }
  if ($0 ~ /^kind:[[:space:]]*EndpointSlice[[:space:]]*$/) {
    doc_is_endpointslice = 1
  }
}

END {
  flush_doc()
}
' "$tmp_input" > "$tmp_input_noeps"

default_namespace="$(awk '/^[[:space:]]*namespace:[[:space:]]*/{print $2; exit}' "$tmp_input")"
if [[ -z "$default_namespace" ]]; then
  default_namespace="default"
fi

# Probe unresolved references from kubediagrams warnings.
docker run --rm -v "$(dirname "$tmp_input")":/work -i "$KUBEDIAGRAMS_IMAGE" \
  kube-diagrams -o "/work/$(basename "$tmp_probe_png")" - < "$tmp_input" \
  > "$tmp_log" 2>&1 || true

declare -A missing_sa=()
declare -A missing_pvc=()
declare -A missing_cm=()
declare -A missing_secret=()
declare -A missing_node=()
declare -A missing_svc=()
declare -A missing_sc=()
declare -A missing_csidriver=()
declare -A missing_pv=()
declare -A missing_ingressclass=()
declare -A missing_gatewayclass=()
declare -A missing_generic_cluster=()
declare -A missing_clusterrole=()
declare -A missing_group=()

while IFS= read -r line; do
  # Pattern like: 'name/namespace/Kind/version' undefined
  if [[ "$line" =~ \'([^\']+)\/([^\']+)\/([^\']+)\/([^\']+)\'\ undefined ]]; then
    ref_name="${BASH_REMATCH[1]}"
    ref_ns="${BASH_REMATCH[2]}"
    ref_kind="${BASH_REMATCH[3]}"
    ref_api="${BASH_REMATCH[4]}"

    case "$ref_kind" in
      ConfigMap)
        missing_cm["$ref_name"]="$ref_ns"
        ;;
      Secret)
        missing_secret["$ref_name|$ref_ns|$ref_api"]=1
        ;;
      ServiceAccount)
        missing_sa["$ref_name"]="$ref_ns"
        ;;
      PersistentVolume)
        missing_pv["$ref_name"]=1
        ;;
      IngressClass)
        missing_ingressclass["$ref_name"]=1
        ;;
      GatewayClass)
        missing_gatewayclass["$ref_name"]=1
        ;;
      *)
        missing_generic_cluster["$ref_name|$ref_kind|$ref_api"]=1
        ;;
    esac
    continue
  fi

  if [[ "$line" =~ ServiceAccount\ \'([^\']+)\'\ undefined ]]; then
    missing_sa["${BASH_REMATCH[1]}"]="$default_namespace"
    continue
  fi

  if [[ "$line" =~ PersistentVolumeClaim\ \'([^\']+)\'\ undefined ]]; then
    missing_pvc["${BASH_REMATCH[1]}"]="$default_namespace"
    continue
  fi

  if [[ "$line" =~ ConfigMap\ \'([^\']+)\'\ undefined ]]; then
    missing_cm["${BASH_REMATCH[1]}"]="$default_namespace"
    continue
  fi

  if [[ "$line" =~ Secret\ \'([^\']+)\'\ undefined ]]; then
    secret_name="${BASH_REMATCH[1]}"
    missing_secret["$secret_name|$default_namespace|v1"]=1
    continue
  fi

  if [[ "$line" =~ Node\ \'([^\']+)\'\ undefined ]]; then
    missing_node["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ Service\ \'([^\']+)\'\ undefined ]]; then
    missing_svc["${BASH_REMATCH[1]}"]="$default_namespace"
    continue
  fi

  if [[ "$line" =~ StorageClass\ \'([^\']+)\'\ undefined ]]; then
    missing_sc["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ PersistentVolume\ \'([^\']+)\'\ undefined ]]; then
    missing_pv["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ IngressClass\ \'([^\']+)\'\ undefined ]]; then
    missing_ingressclass["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ GatewayClass\ \'([^\']+)\'\ undefined ]]; then
    missing_gatewayclass["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ CSIDriver\ \'([^\']+)\'\ undefined ]]; then
    missing_csidriver["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ ClusterRole\ \'([^\']+)\'\ undefined ]]; then
    missing_clusterrole["${BASH_REMATCH[1]}"]=1
    continue
  fi

  if [[ "$line" =~ Group\ \'([^\']+)\'\ undefined ]]; then
    missing_group["${BASH_REMATCH[1]}"]=1
    continue
  fi
done < "$tmp_log"

# For synthetic StorageClasses, use a synthetic CSI provisioner and include its driver.
synthetic_sc_provisioner="stub.csi.k8s.io"
if [[ ${#missing_sc[@]} -gt 0 ]]; then
  missing_csidriver["$synthetic_sc_provisioner"]=1
fi

# Emit normalized YAML first.
cat "$tmp_input"

append_doc() {
  printf '\n---\n'
  cat
}

for name in "${!missing_sa[@]}"; do
  ns="${missing_sa[$name]}"
  append_doc <<DOC
apiVersion: v1
kind: ServiceAccount
metadata:
  name: $name
  namespace: $ns
DOC
done

for name in "${!missing_pvc[@]}"; do
  ns="${missing_pvc[$name]}"
  append_doc <<DOC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: $name
  namespace: $ns
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
DOC
done

for name in "${!missing_cm[@]}"; do
  ns="${missing_cm[$name]}"
  append_doc <<DOC
apiVersion: v1
kind: ConfigMap
metadata:
  name: $name
  namespace: $ns
data: {}
DOC
done

for key in "${!missing_secret[@]}"; do
  IFS='|' read -r name ns api_version <<< "$key"
  append_doc <<DOC
apiVersion: $api_version
kind: Secret
metadata:
  name: $name
  namespace: $ns
type: Opaque
data: {}
DOC
done

for name in "${!missing_node[@]}"; do
  append_doc <<DOC
apiVersion: v1
kind: Node
metadata:
  name: $name
DOC
done

for name in "${!missing_svc[@]}"; do
  ns="${missing_svc[$name]}"
  append_doc <<DOC
apiVersion: v1
kind: Service
metadata:
  name: $name
  namespace: $ns
spec:
  selector: {}
  ports:
    - port: 80
      targetPort: 80
DOC
done

for name in "${!missing_sc[@]}"; do
  append_doc <<DOC
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: $name
provisioner: $synthetic_sc_provisioner
volumeBindingMode: WaitForFirstConsumer
DOC
done

for name in "${!missing_pv[@]}"; do
  append_doc <<DOC
apiVersion: v1
kind: PersistentVolume
metadata:
  name: $name
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  volumeMode: Filesystem
  hostPath:
    path: /tmp/$name
DOC
done

for name in "${!missing_ingressclass[@]}"; do
  append_doc <<DOC
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: $name
spec:
  controller: stub.ingress.k8s.io/controller
DOC
done

for name in "${!missing_gatewayclass[@]}"; do
  append_doc <<DOC
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: $name
spec:
  controllerName: stub.gateway.k8s.io/controller
DOC
done

for key in "${!missing_generic_cluster[@]}"; do
  IFS='|' read -r name kind api_version <<< "$key"
  if rg -Uq "kind: $kind\nmetadata:\n  name: $name" "$tmp_input"; then
    continue
  fi
  append_doc <<DOC
apiVersion: $api_version
kind: $kind
metadata:
  name: $name
DOC
done

for name in "${!missing_clusterrole[@]}"; do
  if rg -Uq "kind: ClusterRole\nmetadata:\n  name: $name" "$tmp_input"; then
    continue
  fi
  append_doc <<DOC
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: $name
rules: []
DOC
done

for name in "${!missing_group[@]}"; do
  if rg -Uq "kind: Group\nmetadata:\n  name: $name" "$tmp_input"; then
    continue
  fi
  append_doc <<DOC
apiVersion: rbac.authorization.k8s.io/v1
kind: Group
metadata:
  name: $name
DOC
done

for name in "${!missing_csidriver[@]}"; do
  append_doc <<DOC
apiVersion: storage.k8s.io/v1
kind: CSIDriver
metadata:
  name: $name
spec:
  attachRequired: false
DOC
done
