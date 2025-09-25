from rest_framework import serializers
from .models import Wallet, Operation

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'name',
        ]

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = [
            'amount', 
            'operation_type', 
            'description',
        ]