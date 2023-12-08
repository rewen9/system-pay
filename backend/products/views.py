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
    def products(self, request: Request):
        """Получить все продукты"""
        res_data = None
        log_func = 'products {}'
        res_status = status.HTTP_200_OK
        
        try:
            res_data = Products.objects.all().values()
        except Exception as er:
            logging.error(log_func.format(er))
            res_data = {'Error': 'Данные некоректны.'}
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(res_data, status=res_status)

    @action(methods=['get'], detail=False)
    def products_max_price(self, request: Request):
        """Получить список продуктов не более указанной суммы"""
        res_status = status.HTTP_200_OK
        log_func = 'get_products_under_max_price {}'
        res_data = None
        
        max_price = request.query_params.get('max_price')
        # Валидация данных
        serializer = PriceSerializer(data={'price': max_price})
        if not serializer.is_valid():
            err = 'Тип данных должен быть числом' if max_price else 'Не передан параметр max_price'
            logging.info(log_func.format(err))
            return Response(
                data={'Error': err},
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            products = Products_price.objects.filter(price__lte=max_price)
            res_data = Products.objects.select_related(
                'products_price', 
                'products_count').filter(
                    id__in=products
                ).values()
                
        except Exception as err:
            logging.info(log_func.format(err))
            res_status = status.HTTP_400_BAD_REQUEST
            res_data = {'Error': 'Данные некоректны.'}
            
        return Response(res_data, status=res_status)


    @action(methods=['POST'], detail=False)
    def product(self, request: Request):
        """Создать новый продукт."""
        log_func = 'product {}'
        res_status = status.HTTP_200_OK
        res_data = None
        
        name = request.query_params.get('name') 
        count = request.query_params.get('count') or 0
        price = request.query_params.get('price') or 0
    
        # Валидация данных        
        if not self._valid_data_product(request):
            return Response(data={'Error': 'Неверный тип данных.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
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
            res_data = {'info':'Продукт добавлен: {}'.format(new_product)}
        except Exception as er:
            logging.info(log_func.format(er))
            res_data = {'Error': 'Данные некоректны.'}
            res_status = status.HTTP_400_BAD_REQUEST
            
        return Response(data=res_data, status=res_status)
    
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