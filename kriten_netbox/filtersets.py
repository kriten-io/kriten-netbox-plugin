from netbox.filtersets import NetBoxModelFilterSet
from .models import KritenRunner, KritenTask, KritenJob

class KritenRunnerFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = KritenRunner
        fields = ('id', 'kriten_cluster', 'name', 'branch', 'giturl', 'image')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)


class KritenTaskFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = KritenTask
        fields = ('id', 'kriten_cluster', 'name', 'runner', 'command')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
    
class KritenJobFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = KritenJob
        fields = ('id', 'kriten_task', 'name', 'owner', 'start_time', 'completion_time')
                 # 'failed', 'completed', 'stdout', 'json_data')

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)