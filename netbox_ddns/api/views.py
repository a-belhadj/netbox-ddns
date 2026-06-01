from netbox.api.viewsets import NetBoxModelViewSet
from ..filtersets import ExtraDNSNameFilterSet
from ..models import ExtraDNSName
from .serializers import ExtraDNSNameSerializer


class ExtraDNSNameViewSet(NetBoxModelViewSet):
    queryset = ExtraDNSName.objects.select_related("ip_address").all()
    serializer_class = ExtraDNSNameSerializer
    filterset_class = ExtraDNSNameFilterSet
