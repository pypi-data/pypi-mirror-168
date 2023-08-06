from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import ProbeSerializer


class ProbeViewSet(NetBoxModelViewSet):
    queryset = models.Probe.objects.prefetch_related('tags', 'device')
    serializer_class = ProbeSerializer
    filterset_class = filtersets.ProbeFilterSet
