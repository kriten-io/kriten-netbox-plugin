from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import KritenCluster, KritenRunner, KritenTask, KritenJob


class NestedKritenClusterSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritencluster-detail'
    )

    class Meta:
        model = KritenCluster
        fields = ('id', 'url', 'display', 'name', 'kriten_url', 'api_token')


class NestedKritenRunnerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritenrunner-detail'
    )

    class Meta:
        model = KritenTask
        fields = ('id', 'url', 'display', 'name', 'branch', 'giturl', 'image', 'secrets')
        
        
class NestedKritenTaskSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritentask-detail'
    )

    class Meta:
        model = KritenTask
        fields = ('id', 'url', 'display', 'name', 'runner', 'command', 'schema', 'synchronous')

class NestedKritenTaskSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritentask-detail'
    )

    class Meta:
        model = KritenTask
        fields = ('id', 'url', 'display', 'name', 'runner', 'command', 'schema', 'synchronous')


class NestedKritenJobSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritenjob-detail'
    )

    class Meta:
        model = KritenJob
        fields = ('id', 'url', 'name', 'owner', 'extra_vars', 'start_time', 'completion_time', 'failed', 'completed', 'stdout', 'json_data')


class KritenClusterSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritencluster-detail'
    )
    #task_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = KritenCluster
        fields = (
            'id', 'url', 'display', 'name', 'kriten_url', 'api_token', 'tags'
        )


class KritenRunnerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritenrunner-detail'
    )
    kriten_cluster = NestedKritenClusterSerializer()

    class Meta:
        model = KritenRunner
        fields = (
            'id', 'url', 'kriten_cluster', 'display', 'name', 'branch', 'giturl', 'image', 'secrets'
        )


class KritenTaskSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritentask-detail'
    )
    kriten_cluster = NestedKritenClusterSerializer()

    class Meta:
        model = KritenTask
        fields = (
            'id', 'url', 'kriten_cluster', 'display', 'name', 'runner', 'command', 'schema', 'synchronous'
        )


class KritenJobSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:kriten_netbox-api:kritenjob-detail'
    )
    kriten_task = NestedKritenTaskSerializer()

    class Meta:
        model = KritenJob
        fields = (
            'id', 'url', 'kriten_task', 'name', 'owner', 'extra_vars', 'start_time', 'completion_time', 'failed', 'completed', 'stdout', 'json_data'
        )