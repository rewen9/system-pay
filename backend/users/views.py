from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request

from backend.users.models import Users, Log
from backend.users.serializer import (
    LogSerializer, 
    UsersSerializer,
    UsersСreateSerializer,
    )

import json
import logging

class RegisterView(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def users(self, request: Request):
        res_data = None
        res_status = status.HTTP_200_OK
        log_func = 'users {}'
        
        try:
            res_data = json.loads(Users.objects.get().__str__())
        except Exception as er:
            res_data = {'Error': 'Данные некоректны.'}
            logging.error(log_func.format(er))
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(res_data, status=res_status)

    @action(methods=['post', 'get'], detail=False)
    def customer(self, request: Request):
        if request.method == 'POST':
            return self._create_customer(request)
        elif request.method == 'GET':
            return self._get_customer(request)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def _create_customer(self, request: Request):
        """Создать нового пользователя."""
        res_status = status.HTTP_200_OK
        log_func = 'Ошибка в _create_customer {}'
        res_data = None
        
        if not request.query_params:
            logging.error(log_func.format('Не переданы параметры'))
            return Response(
                data={'Error': 'Не переданы параметры'},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        name = request.query_params.get('name') 
        company = request.query_params.get('company') 
        
        # валидация данных
        serializer = UsersСreateSerializer(data={
            'name': name,
            'company': company
        })
        if not serializer.is_valid():
            err = 'Данные имя и компания некоректны.'
            logging.error(log_func.format(err))
            return Response(
                data={'Error': err},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        # Если вдруг передали с балансом, то валидация
        balance = request.query_params.get('balance') or 0
        currency = request.query_params.get('balance_currency') or Users.CURRENCY_RUB
        
        serializer = UsersSerializer(data={
            'name': name,
            'company': company,
            'balance': balance,
            'balance_currency': currency
        })
        
        if not serializer.is_valid():
            err = 'Данные баланс и валюта некоректны.'
            logging.error(log_func.format(err))
            return Response(
                data={'Error': err},
                status=status.HTTP_400_BAD_REQUEST,
                )
        
        log_details = f'Пользователь {name} из компании: {company}'
        try:
            Users.register(request.query_params)
            Log.objects.create(
                details=log_details,
                action_description=Log.REGISTER_ACTION_FLAG_CHOICES[Log.REGISTER_SUCCESS_USER]
            )
            res_data = {'info':'Пользователь создан.'}
        except Exception as er:
            res_data = {'Error': 'Данные некоректны.'}
            logging.error(log_func.format(er))
            res_status = status.HTTP_400_BAD_REQUEST
            Log.objects.create(
                details=log_details,
                action_description=Log.REGISTER_ACTION_FLAG_CHOICES[Log.REGISTER_FAILED_USER]
            )
            
        return Response(data=res_data, status=res_status)
    
    def _get_customer(self, request: Request):
        """Получить пользователя по ID"""
        
        res_status = status.HTTP_200_OK
        res_data = None
        log_func = 'Ошибка в _get_customer {}'
        
        try:
            res_data = UsersSerializer(
                            Users.objects.filter(
                                id=request.query_params.get('id')
                                ), 
                                many=True
                            ).data
        except Exception as er:
            res_data = {'Error': 'Данные некоректны.'}
            logging.error(log_func.format(er))
            res_status = status.HTTP_400_BAD_REQUEST
            
        return Response(data=res_data, status=res_status)
    
    
class LogViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Log."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer