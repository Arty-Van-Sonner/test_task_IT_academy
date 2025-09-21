from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Wallet, Operation, Currency
from .serializers import OperationSerializer
from django.shortcuts import get_object_or_404

def wallet_request_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            wallet = get_object_or_404(Wallet, uuid=kwargs['wallet_uuid'])
            kwargs['wallet'] = wallet
        except ValueError:
            return Response({"error": "Invalid UUID format."}, status=status.HTTP_400_BAD_REQUEST)
        response = func(*args, **kwargs)
        if response is None:
            return Response({"error": "BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response
    return wrapper


class WalletOperationView(APIView):
    @wallet_request_wrapper
    def post(self, request, wallet, format=None, *args, **kwargs): 
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            operation_type = validated_data.get('operation_type')
            amount = validated_data.get('amount')
            if operation_type == 'WITHDRAW':
                wallet_balance = wallet.balance
                if wallet_balance < amount:
                    return Response({"error": "There are insufficient funds in the account"}, status=status.HTTP_403_FORBIDDEN)
            operation = serializer.save(wallet=wallet)
            wallet_balance = wallet.balance
            return Response({'wallet': str(wallet), 'balance': wallet_balance}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetWalletBalance(APIView):
    @wallet_request_wrapper
    def get(self, request, wallet, format=None, *args, **kwargs):
        data = {
            'wallet': str(wallet),
            'balance': wallet.balance,
        }
        return Response(data, status=status.HTTP_200_OK)

