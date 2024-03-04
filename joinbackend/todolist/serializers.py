from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import TodoItem,Contacts,TaskAssignments,Subtask,Category
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Contacts

# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User    
        fields = ['id','first_name','last_name']
        
from .models import TodoItem
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category     
        fields = '__all__'

class TodoItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = TodoItem     
        fields = '__all__'
        
class TodoNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem     
        fields = ['id','title']
    
        
class ContactsSerializer(serializers.ModelSerializer): 
      class Meta:
        model = Contacts
        fields = '__all__'
        
class ContactsNameSerializer(serializers.ModelSerializer): 
      class Meta:
        model = Contacts
        fields = ['id','name']
        
class SubtasksSerializer(serializers.ModelSerializer): 
      class Meta:
        model = Subtask
        fields = '__all__'
      
class AssignmentSerializer(serializers.ModelSerializer):
    contact = ContactsNameSerializer (many=False)  
    todoitem = TodoNameSerializer (many=False) 
    class Meta:
        model = TaskAssignments
        #fields = '__all__'
        fields = ['contact','todoitem']

"""
Registers a new User, when all the given data are valid.
Also creates a Contacts object
"""
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }#111abcdefgh
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  def create(self, validated_data):
    print(type(validated_data))
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    contacts = Contacts.objects.create(email = user.email,iconColor="#9327FF",phone = "Phone Number ",name = user.first_name+user.last_name,short =user.first_name[0]+user.last_name[0],user = user)
    return user
  
  # class TodoItemSerializerClass(serializers.ModelSerializer):
  #   def create(self, values):
  #      todo = TodoItem.objects.create(title = values['title'],description= values['description'],date= values['date'],category= values['category'],color= values['color'],checked= values['checked'],prio= values['prio'],state = values['state'])
  #      return todo
