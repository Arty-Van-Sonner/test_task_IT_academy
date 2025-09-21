from django.urls import path
from .views import WalletOperationView, GetWalletBalance

urlpatterns = [
    path('wallets/<str:wallet_uuid>/operation', 
            WalletOperationView.as_view(), name='wallet-operation'),
    path('wallets/<str:wallet_uuid>', 
            GetWalletBalance.as_view(), name='wallet-balance'),
]