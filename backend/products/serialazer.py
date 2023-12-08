from rest_framework import serializers
from .models import (
    Products,
    Products_price,
    Products_count,
    )



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products_price
        fields = ['price']


class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products_count
        fields = ['available_quantity']
