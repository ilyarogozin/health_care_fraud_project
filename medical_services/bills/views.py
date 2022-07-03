import pandas as pd
from django.db.utils import IntegrityError
from django_filters import rest_framework as fl
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .filters import BillFilter
from .fraud_detector import get_fraud_score
from .models import Bill, Client, Organization
from .serializers import BillSerializer, ClientSerializer
from .service_classifier import get_service_class_and_name


class BillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    filter_backends = (fl.DjangoFilterBackend,)
    filterset_class = BillFilter


class ClientViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


@api_view(['POST'])
def upload_client_org(request):
    xlsx_file = request.FILES.get('filename')
    if not xlsx_file:
        return Response(
            {'error': 'файл не загружен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if xlsx_file.name.split('.')[-1] != 'xlsx':
        return Response(
            {'error': 'файл должен быть .xlsx формата'},
            status=status.HTTP_400_BAD_REQUEST
        )
    clients = pd.read_excel(xlsx_file, sheet_name='client')
    organizations = pd.read_excel(xlsx_file, sheet_name='organization')
    for name in clients['name']:
        try:
            Client.objects.create(name=name)
        except IntegrityError:
            continue
    for _, client_name, name, address in organizations.itertuples():
        if address not in ' -\n\t':
            address = 'Адрес: ' + address
        client_name = Client.objects.get(name=client_name)
        try:
            Organization.objects.create(
                client_name=client_name,
                name=name,
                address=address
            )
        except IntegrityError:
            continue
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_bills(request):
    xlsx_file = request.FILES.get('filename')
    if not xlsx_file:
        return Response(
            {'error': 'файл не загружен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if xlsx_file.name.split('.')[-1] != 'xlsx':
        return Response(
            {'error': 'файл должен быть .xlsx формата'},
            status=status.HTTP_400_BAD_REQUEST
        )
    bills = pd.read_excel(xlsx_file, sheet_name='Лист1')
    print(type(bills['date'][0]))
    for _, client_name, client_org, num, sum, timestamp, service in bills.itertuples():
        fraud_score = get_fraud_score(service)
        client_org = Organization.objects.get(name=client_org)
        print(fraud_score)
        if fraud_score >= 0.9:
            client_org.fraud_weight += 1
            client_org.save()
        service_class_name = get_service_class_and_name(service)
        service_class = service_class_name['service_class']
        service_name = service_class_name['service_name']
        client_name = Client.objects.get(name=client_name)
        try:
            Bill.objects.create(
                client_name=client_name,
                client_org=client_org,
                num=num,
                sum=sum,
                date=timestamp.strftime('%d.%m.%Y'),
                service=service,
                service_class=service_class,
                service_name=service_name,
                fraud_score=fraud_score
            )
        except IntegrityError:
            continue
    return Response(status=status.HTTP_200_OK)
