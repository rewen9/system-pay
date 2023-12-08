from rest_framework import serializers
from .models import Transactions as transactions




class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = '__all__'


class TransactionsIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = ['pk']
        
class TransactionsAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = ['amount']
        
        
class TransactionsPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = [
            'customer_id',
            'amount',
            'currency',
            'product',
            'product_quantity',
            ]

class TransactionsCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = ['customer_id']
        