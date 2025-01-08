from netbox.filtersets import NetBoxModelFilterSet
from .models import ExtraDNSName, Server, Zone


class ExtraDNSNameFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = ExtraDNSName
        fields = ('id', 'name', 'ip_address', 'forward_rcode')


class ServerFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Server
        fields = ('id', 'server', 'server_port', 'tsig_key_name', 'tsig_algorithm', "tsig_key")


class ZoneFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Zone
        fields = ('id', 'name', 'ttl', 'server')
