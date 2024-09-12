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
:warning: **Warning** this is incomplete. Django templates are missing.
Workaround was to copy templates/kriten_templates to the netbox-docker directory
and add COPY to Docker-Plugins file.
```
FROM netboxcommunity/netbox:latest

COPY ./plugin_requirements.txt /opt/netbox/
RUN /opt/netbox/venv/bin/pip install  --no-warn-script-location -r /opt/netbox/plugin_requirements.txt
# Copy the missing templates
COPY ./kriten_templates /opt/netbox/netbox/templates/kriten_netbox/
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
docker compose build --no-cache
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

To access netbox go to http://loalhost:8000

