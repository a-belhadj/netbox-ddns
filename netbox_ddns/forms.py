from django import forms
from django.forms import IntegerField

from netbox.forms import NetBoxModelForm, NetBoxModelBulkEditForm
from netbox_ddns.models import ExtraDNSName, Server, Zone
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet


class ZoneForm(NetBoxModelForm):
    class Meta:
        model = Zone
        fields = ('name', 'ttl', 'server')


class ZoneBulkEditForm(NetBoxModelBulkEditForm):
    model = Zone

    ttl = IntegerField(
        min_value=1,
        required=False
    )
    server = DynamicModelChoiceField(
        queryset=Server.objects.all(),
        required=False
    )


class ServerForm(NetBoxModelForm):
    fieldsets = (
        FieldSet('server', 'server_port', name='Server'),
        FieldSet('tsig_key_name', 'tsig_algorithm', "tsig_key", name='Authentication'),
    )

    class Meta:
        model = Server
        fields = ('server', 'server_port', 'tsig_key_name', 'tsig_algorithm', "tsig_key")


class ExtraDNSNameEditForm(NetBoxModelForm):
    class Meta:
        model = ExtraDNSName
        fields = ['name']
