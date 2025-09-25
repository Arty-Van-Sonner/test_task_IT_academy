from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Wallet, Operation, Currency
from .serializers import WalletSerializer, OperationSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class WalletCreateView(APIView):
    @extend_schema(
        summary='Create wallet',
        description='Create a new wallet with the specified name',
        request=WalletSerializer,
        responses={
            201: {'description': 'Successful',},
            400: {'description': 'Bad requerst',},
        } 
    )
    def post(self, request: Request, format=None, *args, **kwargs) -> Response: 
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            new_wallet = serializer.save()
            return Response({'wallet': str(new_wallet)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WalletOperationView(APIView):
    @extend_schema(
        summary='Performing an operation with a wallet',
        description='Performs deposit (DEPOSIT) or withdrawal (WITHDRAW) of funds.',
        request=OperationSerializer,
        examples=[
            OpenApiExample(
                'Example of adding funds to an account',
                summary='Deposit wallet',
                description='Example of a request to replenish a wallet by 1000',
                value={
                    "operation_type": "DEPOSIT",
                    "amount": 1000.0,
                },
                request_only=True,
            ),
            OpenApiExample(
                'Example of withdrawal funds to an account',
                summary='Withdrawal wallet',
                description='Example of a withdrawal request from a 500 wallet',
                value={
                    "operation_type": "WITHDRAW",
                    "amount": 500.0,
                    "description": "Payment"
                },
                request_only=True,
            ),
        ],
        responses={
            201: {'description': 'Successful',},
            400: {'description': 'Bad requerst',},
            403: {'description': 'Insufficient funds',},
            404: {'description': 'Wallet was not found',},
        }
    )
    def post(self, request: Request, wallet_uuid: str, format=None, *args, **kwargs) -> Response:
        print('\n\n', type(request), '\n\n')
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
    @extend_schema(
        summary='Get the wallet balance',
        description='Performs deposit (DEPOSIT) or withdrawal (WITHDRAW) of funds.',
        request=OperationSerializer,
        responses={
            200: {'description': 'Successful',},
            404: {'description': 'Wallet was not found',},
        }
    )
    def get(self, request: Request, wallet_uuid: str, format=None, *args, **kwargs) -> Response:
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        data = {
            'wallet': str(wallet),
            'balance': wallet.balance,
        }
        return Response(data, status=status.HTTP_200_OK)

