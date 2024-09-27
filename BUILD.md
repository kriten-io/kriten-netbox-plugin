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
GitPython
```

Edit Dockerfile-Plugins
```
FROM netboxcommunity/netbox:latest

COPY ./plugin_requirements.txt /opt/netbox/
RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /opt/netbox/plugin_requirements.txt
RUN apt-get update && apt-get install -y git
```

Edit docker-compose.override.yml:
``` yaml
services:
  netbox:
    image: <registry>/<repo>:<tag>
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
docker compose build --no-cache
docker compose up -d
```

Use this command to set the superuser:
```
docker exec -it netbox-docker-netbox-1 python manage.py createsuperuser
```

To access netbox go to http://localhost:8000

To build multi-platform images:

Add additional platforms to docker-compose.override.yml:
``` yaml
services:
  netbox:
    image: <registry>/<repo>:<tag>
    pull_policy: never
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
      platforms:
        - linux/arm64
        - linux/amd64
  netbox-worker:
    image: netbox:latest-plugins
    pull_policy: never
  netbox-housekeeping:
    image: netbox:latest-plugins
    pull_policy: never
```

Login to dockerhub then build:
```
COMPOSE_DOCKER_CLI_BUILD=1 \  
DOCKER_BUILDKIT=1 \
docker compose build --no-cache --push
```

