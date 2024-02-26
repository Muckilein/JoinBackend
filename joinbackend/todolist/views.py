from django.shortcuts import render ,redirect
from rest_framework import viewsets
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TodoItemSerializer,ContactsSerializer,AssignmentSerializer,ContactsNameSerializer,SubtasksSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.http import HttpResponse
from datetime import date
from . methods import *
import json
from django.views.generic.detail import DetailView

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TodoItem.objects.all() #.order_by('date')
    serializer_class = TodoItemSerializer


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
        
"""
Return a JSON of all Contacts
"""       
class ContactsView(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]

    def get(self, request, format=None):
        contacts = Contacts.objects.all()
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)  
    

"""
Registers a User when the given data are correct
"""
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer

"""
Renders the login page
"""
class Logout_view(APIView):
    def get(self, request, format=None):
        logout(request)   
        return Response('ok')
  
    
# def createTodoView(request):   
#     return render(request,'createTask.html')


"""
create: Makes a nuew todo with the given data stored in request.bpdy
get: returns a JSON array with alll the todos
"""
class createTodoViewAPI(generics.CreateAPIView):
    print('call createTodoViewAPI')  
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    #todo = TodoItem.objects.create(title = 'Test1',description="test1",date=date.today(),category='Sales',color='#ab234',checked=False,prio='1',state ='1')
    queryset = TodoItem.objects.all()
    permission_classes = []
    serializer_class = TodoItemSerializer  
    # Create wird automatisch bei POST aufgerufen
    def create(self, request):
         print('call create')
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden 
         data = json.loads(request.body)     
        #todo = TodoItem.objects.create(title = request.POST.get('title'),description=request.POST.get('description'),date=request.POST.get('date'),category=request.POST.get('category'),color=request.POST.get('color'),checked=False,prio=request.POST.get('prio'),state =request.POST.get('state'))
         todo = TodoItem.objects.create(title = data['title'],description=data['description'],date=data['date'],category= data['category'],color= data['color'],checked=False,prio= data['prio'],state = data['state'])
         serializer = TodoItemSerializer(todo, many=False) # wenn hier True stehen würde kommt not iterable error
         todoData = serializer.data
         makeSubtask(data['subtask'],todo)
         makeAssigments(data['assignments'],todo)
         setAssignmentandSubs(todoData)
         return Response(todoData)
    # Wird autimatisch bei GET aufgerufen  
    def get(self, request, format=None):
        todos = TodoItem.objects.all()       
        serializer = TodoItemSerializer(todos, many=True)       
        todoData = serializer.data
        for t in todoData:          
            setAssignmentandSubs(t)              
        return Response(serializer.data) 

"""
get: returns the JSON data of a todo with the given id
put: edits and returns an existing todo with the given id. 
"""
class createTodoViewAPIDetail(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def get(self,request,pk):  #self ist wichtig
        print(pk)
        todos = TodoItem.objects.filter(id = pk)             
        serializer = TodoItemSerializer(todos[0], many=False)       
        todoData = serializer.data#[0]                 
        setAssignmentandSubs(todoData)              
        return Response(todoData)
    def put(self, request,pk):
         print('call put')
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden 
         data = json.loads(request.body)
         todo = TodoItem.objects.filter(id=pk)[0]
         todo.title = data['title']
         todo.description = data['description']
         todo.date = data['date']
         todo.category = data['category']
         todo.prio = data['prio']
         todo.state = data['state']       
         makeSubtask(data['subtask'],todo)
         makeAssigments(data['assignments'],todo)
         todo.save()
         serializer = TodoItemSerializer(todo, many=False)
         todoData = serializer.data
         setAssignmentandSubs(todoData)     
         return Response(todoData)
    def delete(self,request,pk):        
         todo = TodoItem.objects.filter(id=pk)[0]
         resp=todo.delete()         
         return Response(resp)
 
