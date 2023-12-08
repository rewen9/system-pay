from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import mixins, status, viewsets



from backend.transactions.models import Transactions as transactions
from backend.transactions.serialazer import (
    TransactionsAmountSerializer,
    TransactionsPaymentSerializer,
    TransactionsSerializer,
    TransactionsIdSerializer,
    TransactionsCustomerSerializer,
    )

from backend.users.models import Users
from backend.users.views import RegisterView

import json
import logging
from dataclasses import asdict

class TransactionsView(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def transaction_customer(self, request: Request):
        """Получить все транзакции по ID пользователя"""
        log_func = 'Ошибка в transaction_customer {}'
        
        res_data = None
        res_status = status.HTTP_200_OK
        
        # валидация данных
        customer_id = request.query_params.get('customer_id')
        serializer = TransactionsCustomerSerializer(data={
            'customer_id': customer_id
        })
        if not serializer.is_valid():
            err = 'Неверный тип данных.'
            logging.error(log_func.format(err))
            return Response(
                data={'Error': err},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            res_data = transactions.objects.filter(customer_id=customer_id).values()
            if not res_data:
                res_data = {'info': 'Пользователя не существует.'}
        except Exception as err:
            res_data = {'Error': 'Данные некоректны.'}
            logging.error(log_func.format(err))
            res_status = status.HTTP_400_BAD_REQUEST
        
        return Response(res_data, status=res_status)

    @action(methods=['get'], detail=False)
    def transaction(self, request: Request):
        """Получить транзакцию по ID."""
        log_func = 'transaction {}'
        
        res_data = None
        res_status = status.HTTP_200_OK
        request_data = request.query_params.get('id')
        
        # валидация данных
        serializer = TransactionsIdSerializer(data={
            'pk': request_data
        })
        if not serializer.is_valid() or not request_data.isdigit():
            return Response(data={"error": "Неверный тип данных. Должно быть число"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            res_data = TransactionsSerializer(
                            transactions.objects.get(id=request_data)
                        ).data
        except Exception as er:
            logging.error(log_func.format(er))
            res_data = {'Error': 'Транзакция не существует.'}
            res_status = status.HTTP_400_BAD_REQUEST
        
        return Response(res_data, status=res_status)
    
    
    @action(methods=['POST'], detail=False)
    def payment(self, request: Request):
        """Инициализация транзакции."""
        log_func = 'Ошибка в payment {}'
        
        res_data = None
        res_status = status.HTTP_200_OK
        
        customer_id = request.query_params.get('customer_id')
        amount = request.query_params.get('amount')
        currency = request.query_params.get('currency')
        product_quantity = request.query_params.get('product_quantity')  or "not yet"
        product = request.query_params.get('product') or "not yet"
        
        # валидация данных
        serializer = TransactionsPaymentSerializer(data={
            'customer_id': customer_id,
            'amount': amount,
            'currency': currency,
            'product': product,
            'product_quantity': product_quantity,
        })
        
        if not serializer.is_valid():
            err = "Неверный тип данных."
            logging.error(log_func.format(err))
            logging.error(serializer.errors.items())
            return Response(data={"error": err, 'more_info': serializer.errors.items()},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Влидация - Проверка наличия пользователя
        customer = Users.objects.filter(pk=customer_id)
        if not customer.exists(): 
            err = 'Данный пользователь не существует.'
            logging.error(log_func.format(err))
            return Response(
                data={"error": err},
                status=status.HTTP_400_BAD_REQUEST
                ) 
        customer = customer.first()
        # Влидация - Неверный тип валюты
        if customer.balance_currency != currency:
            err = 'Неверный тип валюты пользователя.'
            logging.error(log_func.format(err))
            return Response(
                data={"error": err},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # Валидация - недостарточно средств
        if customer.balance < amount:
            err = 'Недостаточно средств.'
            logging.error(log_func.format(err))
            return Response(
                data={"error": err},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            transactions.create_transaction_new(
                customer_id=customer_id,
                amount=amount,
                currency=currency,
            )
        except Exception as er:
            res_data = {"error": "Неверный тип данных."}
            logging.error(log_func.format(er))
            res_status = status.HTTP_400_BAD_REQUEST
            
        return Response(data=res_data, status=res_status)

    @action(methods=['get'], detail=False)
    def transactions_range_summ(self, request: Request):
        """Получить транзакции в даиапазоне сумм."""
        log_func = 'Ошибка в transactions_range_summ {}'
        res_data = None
        res_status = status.HTTP_200_OK
        
        # валидация данных
        summ_from = request.query_params.get('from')
        summ_to = request.query_params.get('to')
        
        serializer_from = TransactionsAmountSerializer(data={
            'amount': summ_from,
        })
        serializer_to = TransactionsAmountSerializer(data={
            'amount': summ_to,
        })
        
        if not serializer_from.is_valid() or not serializer_to.is_valid():
            log = 'Неверный тип данных.'
            logging.error(log_func.format(log))
            return Response(data={'Error': log}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            res_data = TransactionsSerializer(
                            transactions.objects.filter(
                                amount__range=(summ_from, summ_to)
                            )
                        ).data
            if not res_data:
                res_data = {'info': 'Транзакций не найдено.'}
        except Exception as er:
            logging.error(log_func.format(er))
            res_data = {'Error': 'Данные некоректны.'}
            res_status = status.HTTP_400_BAD_REQUEST
        
        return Response(res_data, status=res_status)
    
    @action(methods=['get'], detail=False)
    def active_currency(self, request: Request):
        """Получить активные валюты."""
        log_func = 'Ошибка в active_currency {}'
        res_data = None
        res_status = status.HTTP_200_OK
        
        try:
            res_data = [choice[1] for choice in Users.CURRENCY_CHOICES]
        except Exception as er:
            res_data = {'Error': 'Данные некоректны.'}
            logging.error(log_func.format(er))
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(res_data, status=res_status)
