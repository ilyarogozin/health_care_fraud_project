from django.urls import path

from .views import BillViewSet, ClientViewSet, upload_bills, upload_client_org

app_name = 'bills'

urlpatterns = [
    path('upload_client_org/', upload_client_org, name='upload_client_org'),
    path('upload_bills/', upload_bills, name='upload_bills'),
    path(
        'get_clients_list/',
        ClientViewSet.as_view({'get': 'list'}),
        name='clients_list'
    ),
    path(
        'get_bills_list/',
        BillViewSet.as_view({'get': 'list'}),
        name='bills_list'
    )
]
