from django.urls import path, include

from utilities.urls import get_model_urls
from .views import ExtraDNSNameCreateView, ExtraDNSNameDeleteView, ExtraDNSNameEditView, IPAddressDNSNameRecreateView, ExtraDNSNameView

urlpatterns = [
    path('zones/', include(get_model_urls('netbox_ddns', 'zone', detail=False))),
    path('zones/<int:pk>/', include(get_model_urls('netbox_ddns', 'zone'))),

    path('servers/', include(get_model_urls('netbox_ddns', 'server', detail=False))),
    path('servers/<int:pk>/', include(get_model_urls('netbox_ddns', 'server'))),
    path(route='ip-addresses/<int:ipaddress_pk>/recreate/',
         view=IPAddressDNSNameRecreateView.as_view(),
         name='ipaddress_dnsname_recreate'),
    path(route='ip-addresses/<int:ipaddress_pk>/extra-dns-name/create/',
         view=ExtraDNSNameCreateView.as_view(),
         name='extradnsname_create'),
    path(route='extra-dns-name/<int:pk>/edit/',
         view=ExtraDNSNameEditView.as_view(),
         name='extradnsname_edit'),
    path(route='extra-dns-name/<int:pk>/delete/',
         view=ExtraDNSNameDeleteView.as_view(),
         name='extradnsname_delete'),
    path(route='extra-dns-name/<int:pk>/',
         view=ExtraDNSNameView.as_view(),
         name='extradnsname'),
]
