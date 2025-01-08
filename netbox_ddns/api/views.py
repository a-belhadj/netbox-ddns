from netbox.api.viewsets import NetBoxModelViewSet
from ..filtersets import ExtraDNSNameFilterSet, ServerFilterSet
from ..models import ExtraDNSName, Server
from .serializers import ExtraDNSNameSerializer, ServerSerializer


class ExtraDNSNameViewSet(NetBoxModelViewSet):
    queryset = ExtraDNSName.objects.all()
    serializer_class = ExtraDNSNameSerializer
    filterset_class = ExtraDNSNameFilterSet


class ServerViewSet(NetBoxModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filterset_class = ServerFilterSet
