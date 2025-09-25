from django.core.management.base import BaseCommand
from settlement_system.models import Currency, Wallet

class Command(BaseCommand):
    def handle(self, *args, **options):
        new_wallet = Wallet.objects.create(name='Test', currency=Currency.default_currency())
        new_wallet.save()