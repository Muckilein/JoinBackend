from django.shortcuts import render ,redirect
from rest_framework import viewsets
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList,Category,User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TodoItemSerializer,ContactsSerializer,CategorySerializer,UserSerializer
#from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.http import HttpResponse
from datetime import date
from . methods import *
import json
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
# class TodoViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = TodoItem.objects.all() #.order_by('date')
#     serializer_class = TodoItemSerializer


"""
Loggs in a user with the given credentials.
Returns a JSON with the token, user_id and email
"""
class LoginView(ObtainAuthToken): 
   def post(self, request, *args, **kwargs):       
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})       
        serializer.is_valid(raise_exception=True)       
        user = serializer.validated_data['user']             
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class GuestExist(APIView):
     def get(self, request):       
        guest = User.objects.filter(email = 'Guest@mail.de')
        if len(guest)>0:
            return Response('YES')
        else:
            return Response('NO')
        
        
     
class ContactsView(APIView):
    """
    Return a JSON of all Contacts
    """  
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]

    def get(self, request,pk):      
        user = request.user  
        contacts = Contacts.objects.filter(user = user)
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)
    def post(self,request,pk):
        data = json.loads(request.body)       
        user = request.user      
        contacts = Contacts.objects.create(email = data['email'],iconColor=data['iconColor'],phone = data['phone'],username = data['username'],short =data['short'],user = user)
        serializer = ContactsSerializer(contacts, many=False)
        return Response(serializer.data)
    def put(self,request,pk):
        data = json.loads(request.body)
        contact = Contacts.objects.filter(id = pk)[0] 
        contact.email = data['email']
        contact.username = data['username']
        contact.phone = data['phone']
        contact.save()
        return Response('ok')
    def delete(self,request,pk):        
         contact = Contacts.objects.filter(id= pk)[0]
         contact.delete()
         return Response('ok')     
    


class RegisterView(generics.CreateAPIView):
    """
    Registers a User when the given data are correct
    """
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer


class Logout_view(APIView):
    """
    Renders the login page
    """
    def get(self, request, format=None):
        logout(request)   
        return Response('ok')
  

class User_viewAPIDetail(APIView):  
    """
    Returns a user with a given primary key
    """  
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def get(self, request,pk):
        print('call get user')
        user = User.objects.filter(id = pk)                  
        serializer = UserSerializer(user, many=True)       
        userData = serializer.data[0] 
        return Response(userData) 
    
class User_viewAPI(APIView): 
    """
    Returns a all users with a given primary key
    """     
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def get(self, request):
        print('call get user')    
        user = User.objects.all()             
        serializer = UserSerializer(user, many=True)       
        userData = serializer.data 
        return Response(userData)     



class createTodoViewAPI(generics.CreateAPIView):
    """
    create: Makes a nuew todo with the given data stored in request.bpdy
    get: returns a JSON array with alll the todos
    """
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    queryset = TodoItem.objects.all()
    permission_classes = []
    serializer_class = TodoItemSerializer  
    # Create wird automatisch bei POST aufgerufen
    def create(self, request):
         print('call create')
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden 
         data = json.loads(request.body) 
         userTodo = request.user
         category = getCategory(data['category']['title'])  
         todo = TodoItem.objects.create(title = data['title'],userTodo = userTodo,description=data['description'],date=data['date'],category= category,color= data['color'],prio= data['prio'],state = data['state'])
         serializer = TodoItemSerializer(todo, many=False) # wenn hier True stehen würde kommt not iterable error
         todoData = serializer.data         
         setCategory = (todoData)
         makeSubtask(data['subtask'],todo)
         makeAssigments(data['assignments'],todo)
         setAssignmentandSubs(todoData)
         return Response(todoData)
    # Wird autimatisch bei GET aufgerufen  
    def get(self, request, format=None):
        userTodo = request.user
        todos = TodoItem.objects.filter(userTodo = userTodo)       
        serializer = TodoItemSerializer(todos, many=True)       
        todoData = serializer.data
        for t in todoData: 
            setCategory(t)       
            setAssignmentandSubs(t)              
        return Response(serializer.data) 


class createTodoViewAPIDetail(APIView):
    """
    get: returns the JSON data of a todo with the given id
    put: edits and returns an existing todo with the given id. 
    """
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):  #self ist wichtig
       
        todos = TodoItem.objects.filter(id = pk)             
        serializer = TodoItemSerializer(todos[0], many=False)       
        todoData = serializer.data#[0]
        setCategory(todoData)                 
        setAssignmentandSubs(todoData)              
        return Response(todoData)
    def put(self, request,pk):       
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden
         data = json.loads(request.body)           
         category = getCategory(data['category']['title'])   
         todo = TodoItem.objects.filter(id=pk)[0]
         todo.title = data['title']
         todo.description = data['description']
         todo.date = data['date']
         todo.color = data['color']
         todo.category = category
         todo.prio = data['prio']
         todo.state = data['state']
         serializer = TodoItemSerializer(todo, many=False) # wenn hier True stehen würde kommt not iterable error
         todoData = serializer.data         
         makeSubtask(data['subtask'],todo)
         #deleteSubtask(data['subtask'],todo)
         makeAssigments(data['assignments'],todo)
         deleteAssigment(data['assignments'],todo)         
         todo.save()
         serializer = TodoItemSerializer(todo, many=False)
         todoData = serializer.data        
         setCategory(todoData)
         setAssignmentandSubs(todoData)     
         return Response(todoData)
    def delete(self,request,pk):        
         todo = TodoItem.objects.filter(id=pk)[0]
         resp=todo.delete()         
         return Response(resp)

def getCategory(t):       
     cat = Category.objects.filter(title = t) 
          
     if len(cat)==0:
         category = Category.objects.create(title= t)
         return category           
     else:        
       category =cat[0]                 
       return category

class categoryAPI(generics.CreateAPIView):
    """
    get: returns the JSON data of all categorys
    create: creates a new category
    """
    queryset = Category.objects.all()
    permission_classes = []
    serializer_class = CategorySerializer
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def create(self,request):
        data = json.loads(request.body)
        print(data)
        category = Category.objects.create(title= data['title'], color = data['color']) 
        categoryData = getSerializedCategory(category,False)     
        return Response(categoryData)
    def get(self,request):
        category = Category.objects.all()         
        categoryData = getSerializedCategory(category,True)                             
        return Response(categoryData)
    
class categoryAPIDetail(APIView):
    """
    get: returns the JSON data of a categoorys with the given id    
    """
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    def get(self,request,pk):
        category = Category.objects.filter(id = pk)           
        categoryData=getSerializedCategory(category[0],False)           
        return Response(categoryData)

