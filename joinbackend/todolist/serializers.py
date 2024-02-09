from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import TodoItem,Contacts,TaskAssignments

# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User    
        fields = ['id','first_name','last_name']
        
from .models import TodoItem
from rest_framework import serializers

class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        #fields = ['id','title']
        fields = '__all__'
        
class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'
        
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignments
        fields = '__all__'



# class TodoSerializer(serializers.HyperlinkedModelSerializer):
#     #user = UserSerializer()
#     #user = serializers.PrimaryKeyRelatedField(read_only = True, default = serializers.CurrentUserDefault())
#     #users = serializers.ListField(child=UserSerializer())
   
#     class Meta:
#         model = TodoItem       
#         fields = ['id','title', 'description', 'date','category' ,'color','prio','state']
