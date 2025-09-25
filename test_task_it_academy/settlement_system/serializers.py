from rest_framework import serializers
from .models import Operation

class OperationSerializer(serializers.ModelSerializer):
    # description = serializers.TextField(read_only=True)
    class Meta:
        model = Operation
        fields = [
            'amount', 
            'operation_type', 
            'description',
        ]