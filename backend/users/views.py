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

    @action(methods=['post'], detail=False)
    def customer(self, request):
        res_status = status.HTTP_400_BAD_REQUEST
        if not request.data:
            return Response(status=res_status)
        
        # перебираем json с данными
        for json_data in request.data:
            name = json_data.get('name') 
            company = json_data.get('company') 
            
            log_details = f'Пользователь {name} из компании: {company}'
            try:
                Users.register(json_data)
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
    
    @action(methods=['get'], detail=False)
    def customer(self, request, *args, **kwargs):
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