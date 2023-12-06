from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

from backend.users.models import Users, Log
from backend.users.serializer import LogSerializer, UsersSerializer

import json

class RegisterView(viewsets.ModelViewSet):
    
    @action(methods=['get'], detail=False)
    def get_users(self, request):
        js = None
        res_status = status.HTTP_200_OK
        
        try:
            js = json.loads(Users.objects.get().__str__())
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        
        return Response(js, status=res_status)

    @action(methods=['post', 'get'], detail=False)
    def customer(self, request):
        if request.method == 'POST':
            return self._create_customer(request)
        elif request.method == 'GET':
            return self._get_customer(request)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def _create_customer(self, request):
        res_status = status.HTTP_400_BAD_REQUEST
        if not request.query_params:
            return Response(status=res_status)
        
        name = request.query_params.get('name') 
        company = request.query_params.get('company') 
        
        log_details = f'Пользователь {name} из компании: {company}'
        try:
            Users.register(request.query_params)
            res_status = status.HTTP_200_OK
            Log.objects.create(
                details=log_details,
                action_description=Log.REGISTER_ACTION_FLAG_CHOICES[Log.REGISTER_SUCCESS_USER]
            )
        except Exception as er:
            Log.objects.create(
                details=log_details,
                action_description=Log.REGISTER_ACTION_FLAG_CHOICES[Log.REGISTER_FAILED_USER]
            )
        return Response(status=res_status)
    
    def _get_customer(self, request):
        """Получить пользователя по ID"""
        user_data = None
        res_status = status.HTTP_200_OK
        
        try:
            user_data = UsersSerializer(
                Users.objects.filter(id=request.query_params.get('id')), many=True
                ).data
        except Exception as er:
            res_status = status.HTTP_404_NOT_FOUND
        return Response(user_data, status=res_status)
    
    
class LogViewSet(viewsets.ModelViewSet):
    """Набор представлений для модели Log."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer