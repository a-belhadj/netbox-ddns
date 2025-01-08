from django import forms

from netbox.forms import NetBoxModelForm
from netbox_ddns.models import ExtraDNSName, Server
from utilities.forms.rendering import FieldSet


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
