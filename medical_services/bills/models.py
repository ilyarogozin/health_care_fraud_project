import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint


class Client(models.Model):
    name = models.CharField(
        verbose_name='Имя клиента',
        max_length=150,
        primary_key=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Organization(models.Model):
    client_name = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Имя клиента'
    )
    name = models.CharField(
        verbose_name='Название организации',
        max_length=200,
        primary_key=True
    )
    address = models.CharField(verbose_name='Адрес', max_length=500)
    fraud_weight = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        constraints = [
            UniqueConstraint(
                fields=['client_name', 'name'],
                name='unique_client_organization'
            )
        ]

    def __str__(self):
        return self.name


def validate_date(value):
    """Проверяем соответствие даты формату 01.01.1111"""
    exp = r'^(\d{2})\.(\d{2})\.(\d{4})$'
    if not bool(re.match(exp, value)):
        raise ValidationError(
            f'Дата - {value} в неправильном формате, должна быть: 01.01.1111'
        )
    return value


class Bill(models.Model):
    client_name = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='bills',
        verbose_name='Имя клиента'
    )
    client_org = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='bills',
        verbose_name='Название организации'
    )
    num = models.PositiveIntegerField(verbose_name='Номер')
    sum = models.FloatField(verbose_name='Сумма')
    date = models.CharField(
        verbose_name='Дата',
        max_length=11,
        validators=[validate_date]
    )
    service = models.CharField(verbose_name='Название услуги', max_length=200)
    service_class = models.PositiveIntegerField(verbose_name='Класс услуги')
    service_name = models.CharField(
        verbose_name='Название класса услуги',
        max_length=200
    )
    fraud_score = models.FloatField(verbose_name='Оценка мошенничества')

    class Meta:
        ordering = ('client_name',)
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        constraints = [
            UniqueConstraint(
                fields=['client_org', 'num'],
                name='unique_num_bills_organization'
            )
        ]
