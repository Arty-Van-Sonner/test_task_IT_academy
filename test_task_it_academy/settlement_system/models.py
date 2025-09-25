import uuid
from typing import Iterable

from django.db import models
from django.db.models import Sum, Case, When, F
from decimal import Decimal

class Currency(models.Model):
    name = models.CharField(max_length=128, help_text='Full name of the currency. For example: "United States Dollar"', default='Test')
    code = models.CharField(max_length=3, unique=True, db_index=True, help_text='ISO 4217. It is a three-letter code. For example: "USD"')
    numeric_code = models.IntegerField(unique=True, db_index=True, help_text='ISO 4217. It is a three-digit numeric currency code. For example: 840')
    symbol = models.CharField(max_length=5, blank=True, help_text='A currency symbol. For example: "$"')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    @staticmethod
    def default_currency():
        queryset = Currency.objects.filter(code='RUB')
        if len(queryset) == 0:
            default_currency = Currency(
                name='Russian Ruble',
                code='RUB',
                numeric_code='643',
                symbol='₽',
                is_active=True,
            )
            default_currency.save()
        else:
            default_currency = queryset.first()
        return default_currency


class Wallet(models.Model):
    name = models.CharField(max_length=256)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} ({self.currency}) [{self.uuid}]'
    
    @property
    def balance(self) -> Decimal:
        balance = self.operations.aggregate(
            total_balance=Sum(
                Case(
                    When(operation_type='DEPOSIT', then=F('amount')),
                    When(operation_type='WITHDRAW', then=-F('amount')),
                    default=0,
                    output_field=models.DecimalField()
                )
            )
        )['total_balance']
        return (balance if balance is not None else Decimal('0')).quantize(Decimal('0.01'))

    @balance.setter
    def balance(self, value):
        self.operations.all().delete()
        new_operation = self.operations.create(amount=value, operation_type='DEPOSIT')
        new_operation.save()

class Operation(models.Model):
    OPERATION_TYPES = [
        ('DEPOSIT', 'DEPOSIT'),
        ('WITHDRAW', 'WITHDRAW'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False, related_name='operations')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount_of_wallet_currency = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # temporary solution
        self.currency = Currency.default_currency()
        self.amount_of_wallet_currency = self.amount
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.operation_type} {self.amount} for {self.wallet}"
