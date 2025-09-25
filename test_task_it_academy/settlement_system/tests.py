from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from settlement_system.models import Wallet, Currency

class SettlementSystemTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create(name='Test', currency=Currency.default_currency())

    def test_deposit(self):
        url = reverse('wallet-operation', args=(self.wallet.uuid,))
        response = self.client.post(url, {'operation_type': 'DEPOSIT', 'amount': 1000}, format='json')
        self.wallet.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 1000.0)
        self.assertEqual(response.data, {'wallet': str(self.wallet), 'balance': 1000})

    def test_withdraw_success(self):
        self.wallet.balance = 1000
        url = reverse('wallet-operation', args=(self.wallet.uuid,))
        response = self.client.post(url, {'operation_type': 'WITHDRAW', 'amount': 500}, format='json')
        self.assertEqual(response.status_code, 201)
        self.wallet.refresh_from_db()
        self.assertEqual(float(self.wallet.balance), 500.0)
        self.assertEqual(response.data, {'wallet': str(self.wallet), 'balance': 500})

    def test_withdraw_insufficient_funds(self):
        url = reverse('wallet-operation', args=(self.wallet.uuid,))
        response = self.client.post(url, {'operation_type': 'WITHDRAW', 'amount': 100}, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': 'There are insufficient funds in the account'})

    def test_get_balance(self):
        self.wallet.balance = 1000
        url = reverse('wallet-balance', args=(self.wallet.uuid,))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'wallet': str(self.wallet), 'balance': 1000})
