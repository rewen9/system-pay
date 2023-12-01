from rest_framework import serializers
from .models import Transactions as transactions




class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = transactions
        fields = '__all__'