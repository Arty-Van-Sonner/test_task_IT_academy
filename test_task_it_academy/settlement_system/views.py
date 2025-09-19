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


class WalletOperationView(APIView):
    @wallet_request_wrapper
    def post(self, request, wallet, format=None, *args, **kwargs): 
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation = serializer.save(wallet=wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetWalletBalance(APIView):
    @wallet_request_wrapper
    def get(self, request, wallet, format=None, *args, **kwargs):
        accept = request.headers.get('Accept', 'unknown').casefold()
        if 'application/json' in accept:
            pass
        elif 'text/html' in accept:
            pass
        else:
            pass
