from django_filters import rest_framework as fl
from django_filters.filters import CharFilter

from .models import Bill


class BillFilter(fl.FilterSet):
    client_name = CharFilter(field_name='client_name__name',
                             lookup_expr='contains')
    client_org = CharFilter(field_name='client_org__name',
                            lookup_expr='contains')

    class Meta:
        model = Bill
        fields = ['client_name', 'client_org']
