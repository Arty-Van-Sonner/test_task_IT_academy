import uuid

from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=128, help_text='Full name of the currency. For example: "United States Dollar"')
    code = models.CharField(max_length=3, unique=True, db_index=True, help_text='ISO 4217. It is a three-letter code. For example: "USD"')
    numeric_code = models.IntegerField(max_length=3, unique=True, db_index=True, help_text='ISO 4217. It is a three-digit numeric currency code. For example: 840')
    symbol = models.CharField(max_length=5, blank=True, help_text='A currency symbol. For example: "$"')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

class Wallet(models.Model):
    name = models.CharField(max_length=256)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.name} ({self.currency})'

class Operation(models.Model):
    OPERATION_TYPES = [
        ('DEPOSIT', 'DEPOSIT'),
        ('WITHDRAWAL', 'WITHDRAWAL'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, default=Currency.objects.get(code='RUB'))
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    amount_of_wallet_currency = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    operation_type = models.CharField(max_length=10, choices=OPERATION_TYPES)
    description = models.TextField(blank=True, null=True)
