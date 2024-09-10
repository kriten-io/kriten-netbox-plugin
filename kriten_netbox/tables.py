import django_tables2 as tables

from netbox.tables import NetBoxTable, columns
from .models import KritenCluster, KritenRunner, KritenTask, KritenJob


class KritenClusterTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    task_count = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = KritenCluster
        fields = ('pk', 'id', 'name', 'runner_count', 'task_count')
        default_columns = ('name', 'runner_count', 'task_count')


class KritenRunnerTable(NetBoxTable):
    kriten_cluster = tables.Column(
        linkify=True
    )
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = KritenRunner
        fields = (
            'pk', 'id', 'kriten_cluster', 'name', 'branch', 'giturl', 'image', 'token'
        )
        default_columns = (
            'kriten_cluster', 'name', 'branch', 'giturl', 'image'     )


class KritenTaskTable(NetBoxTable):
    kriten_cluster = tables.Column(
        linkify=True
    )
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = KritenTask
        fields = (
            'pk', 'id', 'kriten_cluster', 'name', 'runner', 'command', 'schema'
        )
        default_columns = (
            'kriten_cluster', 'name', 'runner', 'command'
        )


class KritenJobTable(NetBoxTable):
    kriten_task = tables.Column(
        linkify=True
    )
    name = tables.Column(
        linkify=True
    )
    actions = columns.ActionsColumn(actions=('delete',))

    class Meta(NetBoxTable.Meta):
        model = KritenJob
        fields = (
            'pk', 'id', 'kriten_task', 'name', 'owner', 'extra_vars', 'start_time', 'completion_time',
            'failed', 'completed', 'stdout', 'json_data'
        )
        default_columns = (
            'kriten_task', 'name', 'owner', 'extra_vars', 'start_time', 'completion_time'
        )