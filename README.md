# Kriten NetBox Plugin

The Kriten NetBox Plugin allows control of Kriten deployments (clusters) from NetBox. You can add clusters, runners, tasks and launch jobs from the plugin.


## kind (Kubernetes) Install

Create a kind configuration file:
``` yaml
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
- role: worker
```

Start cluster:
```
kind create cluster --config cluster-config.yaml
```

Verify  cluster:
```
kubectl get nodes
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   33s   v1.31.0
kind-worker          Ready    <none>          22s   v1.31.0
kind-worker2         Ready    <none>          22s   v1.31.0
```

Helm install NetBox:

:green_circle: **Tip:** To use publicly available image:
```
helm repo add startechnica https://startechnica.github.io/apps

helm install netbox startechnica/netbox \
    --set global.imageRepository=kubecodeio/netbox \
    --set global.imageTag=4.1  \
    --set plugins={kriten_netbox} \
    --set superuser.password=kubecode
```

Helm install Kriten:
```
helm repo add kriten https://kriten-io.github.io/kriten-charts/
helm install kriten kriten/kriten
```

Edit /etc/hosts:
```
# Hostnames must match kubernetes ingress hosts
192.168.1.62    kriten-local
192.168.1.62    netbox-local
```
Install nginx:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Apply the ingress:
``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kriten-netbox-ingress
spec:
  ingressClassName: nginx
  rules:
  - host: kriten-local
    http:
      paths:
      - pathType: Prefix
        path: /
        backend:
          service:
            name: kriten
            port:
              number: 80
  - host: netbox-local
    http:
      paths:
      - pathType: Prefix
        path: /
        backend:
          service:
            name: netbox
            port:
              number: 80
```

Connect to http://kriten-local and http://netbox-local

For information to use [Kriten](https://kriten.io/user_guide/getting_started/)
