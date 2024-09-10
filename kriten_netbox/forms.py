from django import forms
from django.core.exceptions import ValidationError

from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import KritenCluster, KritenRunner, KritenTask, KritenJob
from .services import reach_cluster


class KritenClusterForm(NetBoxModelForm):
    comments = CommentField()

    def clean(self):
        cleaned_data = self.cleaned_data
        kriten_url = cleaned_data.get("kriten_url")
        api_token = cleaned_data.get("api_token")
        name = cleaned_data.get("name")

        if kriten_url and api_token:
            if not reach_cluster(kriten_url=kriten_url, api_token=api_token):
                raise ValidationError(f"Cluster not reachable: {kriten_url}")
            
        # if cluster with different name and same url exists
        if KritenCluster.objects.exclude(name__exact=name).filter(kriten_url__iexact=kriten_url):
            raise ValidationError(f"Cluster with url {kriten_url} already exists")
        
        return super().clean()

    class Meta:
        model = KritenCluster
        fields = ('name', 'kriten_url', 'api_token', 'tags')


class KritenRunnerForm(NetBoxModelForm):
    kriten_cluster = DynamicModelChoiceField(
        queryset=KritenCluster.objects.all()
    )

    class Meta:
        model = KritenRunner
        fields = (
            'kriten_cluster', 'name', 'branch', 'giturl', 'image', 'token', 'secrets'
        )


class KritenRunnerFilterForm(NetBoxModelFilterSetForm):
    model = KritenRunner
    kriten_cluster = forms.ModelMultipleChoiceField(
        queryset=KritenCluster.objects.all(),
        required=False
    )


class KritenTaskForm(NetBoxModelForm):
    kriten_cluster = DynamicModelChoiceField(
        queryset=KritenCluster.objects.all()
    )

    class Meta:
        model = KritenTask
        fields = (
            'kriten_cluster', 'name', 'runner', 'command', 'schema'
        )


class KritenTaskFilterForm(NetBoxModelFilterSetForm):
    model = KritenTask
    kriten_cluster = forms.ModelMultipleChoiceField(
        queryset=KritenCluster.objects.all(),
        required=False
    )

class KritenJobForm(forms.ModelForm):
    kriten_task = DynamicModelChoiceField(
        queryset=KritenTask.objects.all()
    )

    class Meta:
        model = KritenJob
        fields = (
            'kriten_task', 'extra_vars'
        )

class KritenJobFilterForm(NetBoxModelFilterSetForm):
    model = KritenJob
    kriten_task = forms.ModelMultipleChoiceField(
        queryset=KritenTask.objects.all(),
        required=False
    )
