# Setup

! Ubuntu Example. Your distro may vary.
! These instructions (especially the /etc/hosts and ingress parts) are for running this all on a remote VM and connecting via your local machine (Your setup may vary)

## Install Docker

```
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Verify docker installation
sudo systemctl status docker
```

## Install kind

```
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

## Install kubectl

```
sudo snap install kubectl --classic
kubectl version --client
```

## Install helm

```
sudo snap install helm --classic
helm version
```


# Configuration

## Extend the 

## Create a kind configuration file

```
cat <<EOF > cluster-config.yaml
# three node (two workers) cluster config with the control-plane running on 8080 so as not to clash with the Kriten service
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
  - containerPort: 8080      # Move kind control plane to port 8080
    hostPort: 8080
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
- role: worker
EOF
```

## Start cluster:
```
kind create cluster --config cluster-config.yaml
```

## Verify  cluster:
```
kubectl get nodes
NAME                 STATUS   ROLES           AGE   VERSION
kind-control-plane   Ready    control-plane   33s   v1.31.0
kind-worker          Ready    <none>          22s   v1.31.0
kind-worker2         Ready    <none>          22s   v1.31.0
```

## Helm install NetBox with Kriten and Branching plugins

:green_circle: **Tip:** To use publicly available image:
```
helm repo add startechnica https://startechnica.github.io/apps

helm install netbox startechnica/netbox \
    --set global.imageRepository=kubecodeio/netbox \
    --set global.imageTag=4.1  \
    --set plugins={kriten_netbox} \
    --set superuser.password=kubecode
```

## Check the NetBox installation

```
kubectl get pods
```

## Helm install Kriten:
```
helm repo add kriten https://kriten-io.github.io/kriten-charts/
helm install kriten kriten/kriten
```

## Install nginx:
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

## Apply the ingress:
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

## Forward port 80 on the VM to your local machine

- I do this using Visual Studio Code's built-in functionality, but you could also use SSH port forwarding directly

```
ssh -L 8080:localhost:80 your_user@your_vm_public_ip
```

## Edit /etc/hosts on your **local machine**:
```
# Kriten NetBox
127.0.0.1    kriten-local
127.0.0.1    netbox-local
```

## Access NetBox (Alter the port to whichever local port you're forwarding to)

http://netbox-local:57791

## Access Kriten (Alter the port to whichever local port you're forwarding to)

Swagger: http://kriten-local:57791/swagger/index.html

! Note: I haven't figured out how to connect to the Kriten GUI yet. Possibly related to `frontend.enabled` in here: https://kriten.io/#prerequisites-and-guidelines

# Follow the instructions in the README to create the various Kriten elements

https://github.com/mrmrcoleman/kriten-netbox-plugin/blob/main/README.md

# 



Connect to http://kriten-local and 

For information to use [Kriten](https://kriten.io/user_guide/getting_started/)