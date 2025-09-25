from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wallet, Operation, Currency
from .serializers import OperationSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal

class WalletOperationView(APIView):
    def post(self, request, wallet_uuid, format=None, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid) 
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            operation_type = validated_data.get('operation_type')
            amount = Decimal(str(validated_data.get('amount')))
            if operation_type == 'WITHDRAW':
                wallet_balance = wallet.balance
                if wallet_balance < amount:
                    return Response({"detail": "There are insufficient funds in the account"}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(wallet=wallet)
            wallet_balance = wallet.balance
            return Response({'wallet': str(wallet), 'balance': wallet_balance}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetWalletBalance(APIView):
    def get(self, request, wallet_uuid, format=None, *args, **kwargs):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        data = {
            'wallet': str(wallet),
            'balance': wallet.balance,
        }
        return Response(data, status=status.HTTP_200_OK)

