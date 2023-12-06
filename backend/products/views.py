from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request

from dataclasses import asdict

from backend.products.models import (
    Products,
    Products_count,
    Products_price,
    )
from backend.products.serialazer import (
    ProductSerializer,
    PriceSerializer,
    CountSerializer,
    )
    

import json
import logging

class ProductsViewSet(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def get_products(self, request: Request):
        js = None
        res_status = status.HTTP_200_OK
        
        try:
            js = json.loads(Products.objects.get().__str__())
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(js, status=res_status)

    @action(methods=['get'], detail=False, url_path='products_max_price')
    def get_products_under_max_price(self, request: Request):
        """Получить список продуктов не более указанной суммы"""
        res_status = status.HTTP_200_OK
        max_price = request.query_params.get('max_price')
        
        # Валидация данных
        serializer = PriceSerializer(data={'price': max_price})
        if not serializer.is_valid() or not max_price:
            logging.info('ошибка в получении продуктов не более указанной суммы: прислано не число')
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            max_price = request.query_params.get('max_price') or 0
            products = Products_price.objects.filter(price__lte=max_price)
            products = Products.objects.select_related('products_price', 'products_count').filter(
                id__in=products
            )
            
            # Итерируемся по отфильтрованным товарам и получаем нужные данные
            results = []
            for product in products:
                product_data = {
                    'id': product.pk,
                    'name': product.name,
                    'quantity': product.products_count.available_quantity,
                    'price': product.products_price.price,
                }
                results.append(product_data)
        except Exception as err:
            logging.info('ошибка в получении продуктов не более указанной суммы', err)
            res_status = status.HTTP_400_BAD_REQUEST
            
        return Response(results, status=res_status)


    @action(methods=['POST'], detail=False)
    def product(self, request: Request):
        name = request.query_params.get('name') 
        count = request.query_params.get('count') or 0
        price = request.query_params.get('price') or 0
    
        # Валидация данных        
        if not self._valid_data_product(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_product = Products.objects.create(name=name)
            Products_price.objects.create(
                product=new_product,
                price=price
            )
            Products_count.objects.create(
                product=new_product,
                available_quantity=count
            )
            res_status = status.HTTP_200_OK
        except Exception as er:
            logging.info('ошибка в создании продукта', er)
            res_status = status.HTTP_400_BAD_REQUEST
            
        return Response(status=res_status)
    
    def _valid_data_product(self, request: Request):
        
        product_serializer = ProductSerializer(data={
                                'name': request.query_params.get('name')
                                }
                            )
        price_serializer = PriceSerializer(data={
                                'price': request.query_params.get('price')
                                }
                            )
        count_serializer = CountSerializer(data={
                                'available_quantity':  request.query_params.get('count')
                                }
                            )
        
        if product_serializer.is_valid() \
            and price_serializer.is_valid() \
            and count_serializer.is_valid():
                
            return True
        
        return False