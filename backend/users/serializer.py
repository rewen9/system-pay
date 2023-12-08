from rest_framework import serializers
from backend.users.models import Log, Users

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class UsersСreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'company']