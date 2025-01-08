from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _

from ipam.models import IPAddress
from netbox_ddns.background_tasks import dns_create
from netbox_ddns.filtersets import ServerFilterSet, ZoneFilterSet, ReverseZoneFilterSet, ExtraDNSNameFilterSet
from netbox_ddns.forms import ServerForm, ZoneForm, ReverseZoneForm, ExtraDNSNameIPAddressForm, ExtraDNSNameForm
from netbox_ddns.models import DNSStatus, ExtraDNSName, Server, Zone, ReverseZone
from netbox_ddns.tables import ServerTable, ZoneTable, ReverseZoneTable, ExtraDNSNameTable
from netbox_ddns.utils import normalize_fqdn

from netbox.views.generic import ObjectDeleteView, ObjectEditView, ObjectView, ObjectListView, BulkDeleteView

from django.views.generic import View

from utilities.views import register_model_view


# ReverseZone
@register_model_view(ReverseZone)
class ReverseZoneView(ObjectView):
    queryset = ReverseZone.objects.all()


@register_model_view(ReverseZone, 'list', path='', detail=False)
class ReverseZoneListView(ObjectListView):
    queryset = ReverseZone.objects.all()
    table = ReverseZoneTable


@register_model_view(ReverseZone, 'add', detail=False)
@register_model_view(ReverseZone, 'edit')
class ReverseZoneEditView(ObjectEditView):
    queryset = ReverseZone.objects.all()
    form = ReverseZoneForm


@register_model_view(ReverseZone, 'delete')
class ReverseZoneDeleteView(ObjectDeleteView):
    queryset = ReverseZone.objects.all()


@register_model_view(ReverseZone, 'bulk_delete', path='delete', detail=False)
class ReverseZoneBulkDeleteView(BulkDeleteView):
    queryset = ReverseZone.objects.all()
    filterset = ReverseZoneFilterSet
    table = ReverseZoneTable


# Zone
@register_model_view(Zone)
class ZoneView(ObjectView):
    queryset = Zone.objects.all()


@register_model_view(Zone, 'list', path='', detail=False)
class ZoneListView(ObjectListView):
    queryset = Zone.objects.all()
    table = ZoneTable
    filterset = ZoneFilterSet


@register_model_view(Zone, 'add', detail=False)
@register_model_view(Zone, 'edit')
class ZoneEditView(ObjectEditView):
    queryset = Zone.objects.all()
    form = ZoneForm


@register_model_view(Zone, 'delete')
class ZoneDeleteView(ObjectDeleteView):
    queryset = Zone.objects.all()


@register_model_view(Zone, 'bulk_delete', path='delete', detail=False)
class ZoneBulkDeleteView(BulkDeleteView):
    queryset = Zone.objects.all()
    filterset = ZoneFilterSet
    table = ZoneTable


# Server
@register_model_view(Server)
class ServerView(ObjectView):
    queryset = Server.objects.all()


@register_model_view(Server, 'list', path='', detail=False)
class ServerListView(ObjectListView):
    queryset = Server.objects.all()
    table = ServerTable
    filterset = ServerFilterSet


@register_model_view(Server, 'add', detail=False)
@register_model_view(Server, 'edit')
class ServerEditView(ObjectEditView):
    queryset = Server.objects.all()
    form = ServerForm


@register_model_view(Server, 'delete')
class ServerDeleteView(ObjectDeleteView):
    queryset = Server.objects.all()


@register_model_view(Server, 'bulk_delete', path='delete', detail=False)
class ServerBulkDeleteView(BulkDeleteView):
    queryset = Server.objects.all()
    filterset = ServerFilterSet
    table = ServerTable


# ExtraDNSName
@register_model_view(ExtraDNSName)
class ExtraDNSNameView(ObjectView):
    queryset = ExtraDNSName.objects.all()


@register_model_view(ExtraDNSName, 'list', path='', detail=False)
class ExtraDNSNameListView(ObjectListView):
    queryset = ExtraDNSName.objects.all()
    table = ExtraDNSNameTable
    filterset = ExtraDNSNameFilterSet


@register_model_view(ExtraDNSName, 'add', detail=False)
class ExtraDNSNameEditView(ObjectEditView):
    queryset = ExtraDNSName.objects.all()
    form = ExtraDNSNameForm


@register_model_view(ExtraDNSName, 'edit')
class ExtraDNSNameEditView(ObjectEditView):
    queryset = ExtraDNSName.objects.all()
    form = ExtraDNSNameIPAddressForm


@register_model_view(ExtraDNSName, 'delete')
class ExtraDNSNameDeleteView(ObjectDeleteView):
    queryset = ExtraDNSName.objects.all()

    def get_return_url(self, request, obj=None):
        if obj and obj.ip_address:
            return obj.ip_address.get_absolute_url()
        return super().get_return_url(request, obj)


@register_model_view(ExtraDNSName, 'bulk_delete', path='delete', detail=False)
class ExtraDNSNameBulkDeleteView(BulkDeleteView):
    queryset = ExtraDNSName.objects.all()
    filterset = ExtraDNSNameFilterSet
    table = ExtraDNSNameTable


class ExtraDNSNameCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'netbox_ddns.add_extradnsname'
    queryset = ExtraDNSName.objects.all()
    form = ExtraDNSNameIPAddressForm

    def get_object(self, *args, **kwargs):
        ip_address = get_object_or_404(IPAddress, pk=kwargs['ipaddress_pk'])
        return ExtraDNSName(ip_address=ip_address)


class IPAddressDNSNameRecreateView(PermissionRequiredMixin, View):
    permission_required = 'ipam.change_ipaddress'

    # noinspection PyMethodMayBeStatic
    def post(self, request, ipaddress_pk):
        ip_address = get_object_or_404(IPAddress, pk=ipaddress_pk)

        new_address = ip_address.address.ip
        new_dns_name = normalize_fqdn(ip_address.dns_name)

        updated_names = []

        if new_dns_name:
            status, created = DNSStatus.objects.get_or_create(ip_address=ip_address)

            dns_create.delay(
                dns_name=new_dns_name,
                address=new_address,
                status=status,
            )

            updated_names.append(new_dns_name)

        for extra in ip_address.extradnsname_set.all():
            new_address = extra.ip_address.address.ip
            new_dns_name = extra.name

            dns_create.delay(
                dns_name=new_dns_name,
                address=new_address,
                status=extra,
                reverse=False,
            )

            updated_names.append(new_dns_name)

        if updated_names:
            messages.info(request, _("Updating DNS for {names}").format(names=', '.join(updated_names)))

        return redirect('ipam:ipaddress', pk=ip_address.pk)
