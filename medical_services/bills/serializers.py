from django.db.models import Sum
from rest_framework import serializers

from .models import Bill, Client


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = (
            'client_name', 'client_org', 'num', 'sum',
            'date', 'service', 'service_class', 'service_name', 'fraud_score'
        )


class ClientSerializer(serializers.ModelSerializer):
    num_of_organizations = serializers.SerializerMethodField()
    sum_of_bills = serializers.SerializerMethodField()

    def get_num_of_organizations(self, client):
        return client.organizations.count()

    def get_sum_of_bills(self, client):
        return client.bills.aggregate(sum=Sum('sum'))['sum']

    class Meta:
        model = Client
        fields = ('name', 'num_of_organizations', 'sum_of_bills')
