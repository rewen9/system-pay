from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

from backend.products.models import (
    Products,
    Products_count,
    Products_price,
    )
from backend.products.serialazer import ProductSerializer

import json
import logging

class ProductsViewSet(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def get_products(self, request):
        js = None
        res_status = status.HTTP_200_OK
        
        try:
            js = json.loads(Products.objects.get().__str__())
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(js, status=res_status)

    @action(methods=['get'], detail=False, url_path='products_max_price')
    def get_products_under_max_price(self, request):
        """Получить список продуктов не более указанной суммы"""
        res_status = status.HTTP_200_OK
        
        try:
            max_price = request.query_params.get('max_price') or 0
            products = Products_price.objects.filter(price__lte=max_price)
            products = Products.objects.select_related('products_price', 'products_count').filter(
                id__in=products
            )
            results = []
            # Итерируемся по отфильтрованным товарам и получаем нужные данные
            for product in products:
                product_data = {
                    'id': product.pk,
                    'name': product.name,
                    'quantity': product.products_count.available_quantity,
                    'price': product.products_price.price,
                }
                results.append(product_data)
        except Exception as err:
            res_status = status.HTTP_400_BAD_REQUEST
        return Response(results, status=res_status)


    @action(methods=['POST'], detail=False)
    def product(self, request):
        for js_data in request.data:
            name = js_data.get('name') 
            count = js_data.get('count') or 0
            price = js_data.get('price') or 0
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
    
    