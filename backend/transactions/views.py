from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets

from backend.transactions.models import Transactions as transactions
from backend.transactions.serialazer import TransactionsSerializer

from backend.users.models import Users
import json
import logging

class TransactionsView(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def transaction_an_customer(self, request):
        js = None
        res_status = status.HTTP_200_OK
        
        try:
            js = json.dumps(transactions.objects.filter(customer_id=request['customer_id']))
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(js, status=res_status)

    @action(methods=['get'], detail=False, url_path='transaction')
    def transaction_an_id(self, request):
        res_data = None
        res_status = status.HTTP_200_OK
        request_data = request.query_params.get('id')
        try:
            if request_data:
                res_data = TransactionsSerializer(
                                transactions.objects.filter(id=request_data).first()
                            ).data
                
        except Exception as er:
            logging.error(er)
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(res_data, status=res_status)
    
    
    @action(methods=['POST'], detail=False)
    def payment(self, request):
        res_status = status.HTTP_200_OK
        try:
            for request_data in request.data:
                transactions.create_transaction_new(
                    customer_id=request_data.get('customer_id'),
                    amount=request_data.get('amount'),
                    currency=request_data.get('currency'),
                )
        except Exception as er:
            logging.error(er)
            res_status = status.HTTP_404_NOT_FOUND
        return Response(status=res_status)

    @action(methods=['get'], detail=False)
    def transaction_an_summ(self, request):
        """Получить транзакции в даиапазоне сумм."""
        js = None
        res_status = status.HTTP_200_OK
        
        try:
            js = json.dumps(transactions.objects.filter(
                amount__range=(request['from'], request['to'])
                ))
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(js, status=res_status)
    
    @action(methods=['get'], detail=False)
    def active_currency(self, request):
        """Получить активные валюты."""
        res_data = None
        res_status = status.HTTP_200_OK
        try:
            values = [choice[1] for choice in Users.CURRENCY_CHOICES]
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(values, status=res_status)
