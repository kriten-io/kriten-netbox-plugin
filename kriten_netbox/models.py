import json
import logging
import random
import requests
import string

from django.contrib import messages
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

class KritenCluster(NetBoxModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    kriten_url = models.CharField(
        max_length=100
    )
    api_token = models.CharField(
        max_length=64
    )
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:kriten_netbox:kritencluster', args=[self.pk])


class KritenRunner(NetBoxModel):
    kriten_cluster = models.ForeignKey(
        to=KritenCluster,
        on_delete=models.CASCADE,
        related_name='runners'
    )
    name = models.CharField(
        max_length=100
    )
    branch = models.CharField(
        max_length=100
    )
    image = models.CharField(
        max_length=100
    )
    giturl = models.URLField(
        max_length=200
    )
    token = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    secrets = models.JSONField(
        blank=True,
        null=True,
        default=dict
    )

    def save(self, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectDeleteView')
        kriten_url = self.kriten_cluster.kriten_url
        kriten_token = self.kriten_cluster.api_token
        headers = {
            "Content-Type": "application/json",
            "Token": kriten_token
        }
        body = {
            "name": self.name,
            "branch": self.branch,
            "image": self.image,
            "giturl": self.giturl,
            "token": self.token,
            "secret": self.secrets
        }
        payload = json.dumps(body)
        runner_url = f"{kriten_url}/api/v1/runners/"
        this_runner_url = runner_url + self.name
        try:
            check_runner = requests.get(this_runner_url, headers=headers)
            if check_runner.status_code == 200:
                # Patch task
                patch_runner = requests.patch(this_runner_url, headers=headers, data=payload)
                if patch_runner.status_code != 200:
                    # Patch failed
                    logger.warning(f"Failed to patch runner {self.name} to {kriten_url}.")
        except Exception as e:
            logger.warning(f"Failed to patch runner {self.name} {str(e)}.")
        else:
            try:
                save_runner = requests.post(runner_url, headers=headers, data=payload)
                if save_runner.status_code != 200:
                    # Save failed
                    logger.warning(f"Failed to save runner {self.name} to {kriten_url}.")
            except Exception as e:
                logger.warning(f"Failed to save runner {self.name} {str(e)}.")
        super(KritenRunner, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectDeleteView')
        kriten_url = self.kriten_cluster.kriten_url
        kriten_token = self.kriten_cluster.api_token
        runner_url = f"{kriten_url}/api/v1/runners/"
        this_runner_url = runner_url + self.name
        headers = {
            "Content-Type": "application/json",
            "Token": kriten_token
        }
        try:
            delete_runner = requests.delete(this_runner_url, headers=headers)
            if delete_runner.status_code != 200:
                # Delete failed
                logger.warning(f"Failed to delete runner {self.name} from {kriten_url}.")
        except Exception as e:
            logger.warning(f"Failed to delete runner {self.name} from {str(e)}.")
        super(KritenRunner, self).delete(*args, **kwargs)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:kriten_netbox:kritenrunner', args=[self.pk])
    

class KritenTask(NetBoxModel):
    kriten_cluster = models.ForeignKey(
        to=KritenCluster,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    name = models.CharField(
        max_length=100
    )
    runner = models.ForeignKey(
        to=KritenRunner,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    command = models.CharField(
        max_length=200
    )
    schema = models.JSONField(
        blank=True,
        null=True,
        default=dict
    )
    synchronous = models.BooleanField(
        blank=True,
        default=False
    )

    def save(self, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectDeleteView')
        kriten_url = self.kriten_cluster.kriten_url
        kriten_token = self.kriten_cluster.api_token
        headers = {
            "Content-Type": "application/json",
            "Token": kriten_token
        }
        body = {
            "name": self.name,
            "runner": self.runner.name,
            "command": self.command,
            "schema": self.schema
        }
        payload = json.dumps(body)
        task_url = f"{kriten_url}/api/v1/tasks/"
        this_task_url = task_url + self.name
        check_task = requests.get(this_task_url, headers=headers)
        if check_task.status_code == 200:
            # Patch task
            patch_task = requests.patch(this_task_url, headers=headers, data=payload)
            if patch_task.status_code != 200:
                logger.warning(f"Failed to patch task {self.name} to {kriten_url}.")
        else:
            try:
                save_task = requests.post(task_url, headers=headers, data=payload)
                if save_task.status_code != 200:
                    # Save failed
                    logger.warning(f"Failed to save task {self.name} to {kriten_url}.")
            except Exception as e:
                logger.warning(f"Failed to save task {self.name}: {str(e)}.")
        super(KritenTask, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger = logging.getLogger('netbox.views.ObjectDeleteView')
        kriten_url = self.kriten_cluster.kriten_url
        kriten_token = self.kriten_cluster.api_token
        task_url = f"{kriten_url}/api/v1/tasks/"
        this_task_url = task_url + self.name
        headers = {
            "Content-Type": "application/json",
            "Token": kriten_token
        }
        try:
            delete_task = requests.delete(this_task_url, headers=headers)
            if delete_task.status_code != 200:
                # Delete failed
                logger.warning(f"Failed to delete task {self.name} from {kriten_url}.")
        except Exception as e:
            logger.warning(f"Failed to delete task {self.name}: {str(e)}.")
        super(KritenTask, self).delete(*args, **kwargs)


    class Meta:
        ordering = ('kriten_cluster', 'name')
        unique_together = ('kriten_cluster', 'name')

    def __str__(self):
        #return f'{self.kriten_cluster}: KritenTask {self.name}'
        return f'{self.kriten_cluster}:{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:kriten_netbox:kritentask', args=[self.pk])

class KritenJob(NetBoxModel):
    kriten_task = models.ForeignKey(
        to=KritenTask,
        on_delete=models.CASCADE,
        related_name='kritenjobs'
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='not_launched'
    )
    owner = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    extra_vars = models.JSONField(
        blank=True,
        null=True,
        default=dict
    )
    start_time = models.DateTimeField(
        blank=True,
        null=True
    )
    completion_time = models.DateTimeField(
        blank=True,
        null=True
    )
    failed = models.SmallIntegerField(
        blank=True,
        default=0
    )
    completed = models.SmallIntegerField(
        blank=True,
        default=0
    )
    stdout = models.CharField(
        max_length=50000,
        blank=True,
        null=True
    )
    json_data = models.JSONField(
        blank=True,
        null=True
    )

    def launch_job(self):
        kriten_task_name = self.kriten_task.name
        kriten_url = self.kriten_task.kriten_cluster.kriten_url
        kriten_token = self.kriten_task.kriten_cluster.api_token
        headers = {
            "Content-Type": "application/json",
            "Token": kriten_token
        }
        payload = json.dumps(self.extra_vars)
        launch_url = f"{kriten_url}/api/v1/jobs/{kriten_task_name}"
        launch = requests.request("POST",launch_url, headers=headers, data=payload)
        print("LAUNCH:", launch.content)
        if launch.status_code == 200:
            job_id = launch.json()["id"]
        else:
            launch_json = launch.json()
            unique_hash = ''.join(random.choices(string.ascii_letters,k=5))
            launch_json["hash"] = unique_hash
            job_id = launch_json
        self.name = job_id
        return

    def save(self, *args, **kwargs):
        if not self.completed:
            self.launch_job()
        super(KritenJob, self).save(*args, **kwargs)



    class Meta:
        ordering = ('-start_time',)
        unique_together = ('kriten_task', 'name')

    def __str__(self):
        #return f'{self.kriten_task}: KritenJob {self.name}'
        return f'{self.kriten_task}:{self.name}'

    def get_absolute_url(self):
        return reverse('plugins:kriten_netbox:kritenjob', args=[self.pk])