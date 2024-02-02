from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import TodoItem

# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User    
        fields = ['id','first_name','last_name']

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    #user = UserSerializer()
    #user = serializers.PrimaryKeyRelatedField(read_only = True, default = serializers.CurrentUserDefault())
    users = serializers.ListField(child=UserSerializer())
   
    class Meta:
        model = TodoItem       
        fields = ['id','title', 'description', 'date']
