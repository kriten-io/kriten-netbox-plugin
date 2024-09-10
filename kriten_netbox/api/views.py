from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import KritenClusterSerializer, KritenRunnerSerializer, KritenTaskSerializer, KritenJobSerializer


class KritenClusterViewSet(NetBoxModelViewSet):
    queryset = models.KritenCluster.objects.prefetch_related('tags').annotate(
        task_count=Count('tasks')
    )

    serializer_class = KritenClusterSerializer


class KritenRunnerViewSet(NetBoxModelViewSet):
    queryset = models.KritenRunner.objects.prefetch_related(
         'kriten_cluster', 'tags'
    )
    
    serializer_class = KritenRunnerSerializer
    filterset_class = filtersets.KritenRunnerFilterSet


class KritenTaskViewSet(NetBoxModelViewSet):
    queryset = models.KritenTask.objects.prefetch_related(
         'kriten_cluster', 'tags'
    )

    serializer_class = KritenTaskSerializer
    filterset_class = filtersets.KritenTaskFilterSet


class KritenJobViewSet(NetBoxModelViewSet):
    queryset = models.KritenJob.objects.prefetch_related(
         'kriten_task', 'tags'
    )

    serializer_class = KritenJobSerializer
    filterset_class = filtersets.KritenJobFilterSet