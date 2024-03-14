from django.shortcuts import render ,redirect
from rest_framework import viewsets
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList,Category
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TodoItemSerializer,ContactsSerializer,CategorySerializer
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
class LoginView2(ObtainAuthToken): 
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
        
class LoginView(ObtainAuthToken): 
   def post(self, request, *args, **kwargs):
      loginClass = EmailOrUsernameAuthentication();
      data = loginClass.auth(self,request)
      return Response(data)
        
"""
Return a JSON of all Contacts
"""       
class ContactsView(APIView):
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]

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
         category = getCategory(data['category']['title'])    
        #todo = TodoItem.objects.create(title = request.POST.get('title'),description=request.POST.get('description'),date=request.POST.get('date'),category=request.POST.get('category'),color=request.POST.get('color'),checked=False,prio=request.POST.get('prio'),state =request.POST.get('state'))
         todo = TodoItem.objects.create(title = data['title'],description=data['description'],date=data['date'],category= category,color= data['color'],checked=False,prio= data['prio'],state = data['state'])
         serializer = TodoItemSerializer(todo, many=False) # wenn hier True stehen würde kommt not iterable error
         todoData = serializer.data
         setCategory = (todoData)
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
            setCategory(t)       
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
       
        todos = TodoItem.objects.filter(id = pk)             
        serializer = TodoItemSerializer(todos[0], many=False)       
        todoData = serializer.data#[0]
        setCategory(todoData)                 
        setAssignmentandSubs(todoData)              
        return Response(todoData)
    def put(self, request,pk):
         print('call put')
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden
         
         data = json.loads(request.body)
         print(data)      
         category = getCategory(data['category']['title'])        
       
         todo = TodoItem.objects.filter(id=pk)[0]
         todo.title = data['title']
         todo.description = data['description']
         todo.date = data['date']
         todo.category = category
         todo.prio = data['prio']
         todo.state = data['state']       
         makeSubtask(data['subtask'],todo)
         deleteSubtask(data['subtask'],todo)
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
    queryset = Category.objects.all()
    permission_classes = []
    serializer_class = CategorySerializer
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    
    def create(self,request):
        data = json.loads(request.body)
        category = Category.objects.create(title= data['title'], color = data['color']) 
        categoryData = getSerializedCategory(category,False)     
        return Response(categoryData)
    def get(self,reqiest):
        category = Category.objects.all()         
        categoryData = getSerializedCategory(category,True)                      
        return Response(categoryData)
    
class categoryAPIDetail(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    def get(self,request,pk):
        category = Category.objects.filter(id = pk)           
        categoryData=getSerializedCategory(category[0],False)           
        return Response(categoryData)


class EmailOrUsernameAuthentication(authentication.BaseAuthentication):
   # def authenticate(self, request):
    def auth(self, request):
        # Versuchen Sie zuerst, Benutzer per E-Mail zu authentifizieren
        email = request.data.get('email')
        User = get_user_model()
        if email:
            try:
                  user = User.objects.get(email=email)
                  token, created = Token.objects.get_or_create(user=user)
                  return Response({
                   'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                     })
                
            except User.DoesNotExist:
                pass

        # Falls keine Übereinstimmung gefunden wurde, versuchen Sie es mit dem Benutzernamen
        # username = request.data.get('username')
        # if username:
        #     try:
        #         user = User.objects.get(username=username)
        #         return (user, None)
        #     except User.DoesNotExist:
        #         pass

        # Wenn weder E-Mail noch Benutzername angegeben wurden oder keine Übereinstimmung gefunden wurde,
        # geben Sie eine Authentifizierungsfehlermeldung zurück
        raise exceptions.AuthenticationFailed('Unable to authenticate with provided credentials.')