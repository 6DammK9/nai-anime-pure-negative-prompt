# Making KubeDiagram actually showing deployed systems #

*The intention remains hidden. BTW I think it counts for "AI art".*

The codes here are obviously vibe-coded. I know piping YAML contents is a solid idea, but I can't handle the $O(N^2)$ of content mapping, especially I'm not proficient in k8s.

Also, [it requires you use k8s namespaces to manage resources](https://www.vcluster.com/blog/kubernetes-namespace-the-what-why-and-how), and at least know the basic input / output across k8s CLI. ~~Google it and look for AI summary. It does a good job in this topic.~~

```sh
kubectl krew install get-all
docker pull philippemerle/kubediagrams

# Run "kubctl get-all" except "kubctl get all" for namespace "kube-system" which crash the kube-diagrams.
sh ./make-svg-per-ns.sh
```

Since it is easy to turn it generating Mermaid files, I omit the script. See [dbgate-system.mermaid](./dbgate-system.mermaid) for result. *Github can preview it directly.*

Here is a minimal version generated from [steveteuber/kubectl-graph](https://github.com/steveteuber/kubectl-graph) and trimmed manually.

```mermaid
graph 
  7cb1fe40-eee3-472d-9218-7864d2872330((k8s-master)):::Node
  8aecafaf-dc07-40fa-a660-f0a336003e31((k8s-worker1)):::Node
  47a37386-6dc5-4de1-867f-c676187c9e37((k8s-worker2)):::Node

  4ca77eca-a3be-4d39-8d9b-bdb68472145d((csi-node-driver-q8z47)):::Pod
  235fc504-78e6-4d85-8c14-f7161cb22def((csi-node-driver-wsh9c)):::Pod
  13c644e4-b95e-4e04-94aa-a7bf40ae9361((csi-node-driver-q57dl)):::Pod

  16890be6-e5b0-45f4-9099-ac787bedaa75((csi-node-driver)):::DaemonSet

  16890be6-e5b0-45f4-9099-ac787bedaa75 -- Pod --> 4ca77eca-a3be-4d39-8d9b-bdb68472145d
  16890be6-e5b0-45f4-9099-ac787bedaa75 -- Pod --> 235fc504-78e6-4d85-8c14-f7161cb22def
  16890be6-e5b0-45f4-9099-ac787bedaa75 -- Pod --> 13c644e4-b95e-4e04-94aa-a7bf40ae9361

  4ca77eca-a3be-4d39-8d9b-bdb68472145d -- Node --> 7cb1fe40-eee3-472d-9218-7864d2872330
  235fc504-78e6-4d85-8c14-f7161cb22def -- Node --> 8aecafaf-dc07-40fa-a660-f0a336003e31
  13c644e4-b95e-4e04-94aa-a7bf40ae9361 -- Node --> 47a37386-6dc5-4de1-867f-c676187c9e37
```

## Extra: Migrate Ingress into HTTPRoutes ##

The codes here are obviously vibe-coded too. I do admire that [higress](https://higress.ai/en/blog/higress-gvr7dx_awbbpb_vbzalyy37xxuoswm/) glue things quite well, even the terminology is a mess. ~~"MCP Bridge" is a riddle to solve.~~

```sh
kubectl get ingress -A -o yaml > ingress.yaml
python3 ingress-httproute.py ingress.yaml -o httproute.yaml

# All Gateway API related resources, across namespace. Ignore warnings (out scope).
./get-all-gateway-apis.sh | ./fill-references-stubonly.sh | docker run -v "$(pwd)":/work -i philippemerle/kubediagrams kube-diagrams -f svg --embed-all-icons -o all-gateway-apis.svg -
```

![all-gateway-apis.svg](./all-gateway-apis.svg)

Imagine how `higress-system.svg` looks like.

![26081001.png](./26081001.png)
