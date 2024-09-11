# Kriten NetBox Plugin

The Kriten NetBox Plugin allows control of Kriten deployments (clusters) from NetBox. You can add clusters, runners, tasks and launch jobs from the plugin.

To utilize plugins that have been created by users within the [NetBox Community](https://github.com/netbox-community/netbox/wiki/Plugins) a custom Docker image must be created. 

NetBox instructions to build and deploy plugins [Using NetBox Plugins](https://github.com/netbox-community/netbox-docker/wiki/Using-Netbox-Plugins)

## Docker Install

```
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
touch plugin_requirements.txt Dockerfile-Plugins docker-compose.override.yml
```

Edit plugin_requirements.txt:
```
kriten-netbox
```

Edit Dockerfile-Plugins:
```
FROM netboxcommunity/netbox:latest

COPY ./plugin_requirements.txt /opt/netbox/
RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /opt/netbox/plugin_requirements.txt
```

Edit docker-compose.override.yml:
``` yaml
services:
  netbox:
    image: netbox:latest-plugins
    pull_policy: never
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
  netbox-worker:
    image: netbox:latest-plugins
    pull_policy: never
  netbox-housekeeping:
    image: netbox:latest-plugins
    pull_policy: never
```

Edit configuration/configuration.py:
``` python
PLUGINS = [“kriten_netbox”]
```

Docker build and start:
```
docker compose build —no-cache
docker compose up -d
```

Use this command to set the super user:
```
docker exec -it netbox-docker-netbox-1 python manage.py createsuperuser
```

If you want to use this image on Kubernetes:
```
docker tag netbox:latest-plugins <your_repository>/<image_name>:<image_tag>
docker push <your_repository>/<image_name>:<image_tag>
```

## kind (Kubernetes) Install

Create a kind configuration file:
``` yaml
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
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
```
helm repo add startechnica https://startechnica.github.io/apps

helm install netbox startechnica/netbox \
    --set global.imageRepository=<your_repository>/<image_name> \
    --set global.imageTag=<image_tag>  \
    --set plugins={kriten_netbox} \
    --set superuser.password=<password>
```
:green_circle: **Tip:** To use publicly available image:
```
helm install netbox startechnica/netbox \
    --set global.imageRepository=kubecodeio/netbox \
  --set global.imageTag=4.1  \
    --set plugins={kriten_netbox} \
    --set superuser.password=kubecode
```
