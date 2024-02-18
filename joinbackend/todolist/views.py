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
import json

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TodoItem.objects.all() #.order_by('date')
    serializer_class = TodoItemSerializer

        
def getContactsbyId(id):
    contact = Contacts.objects.all()
    serializerContact = ContactsNameSerializer(contact, many=True)
    contactData = serializerContact.data
    for c in  contactData:
        if c['id']==id:
          return c['name'] 
    return ''  

def getSubtaskbyId(id):
    subs = Subtask.objects.all()
    subSerilizer =  SubtasksSerializer(subs,many=True)      
    subData = subSerilizer.data             
    for s in  subData:
        if s['id']==id:
          return {'title':s['title'] , 'checked': s['checked']}
    return  {'title':'' , 'checked': False}  
    
   

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
        
        
class ContactsView(APIView):
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]

    def get(self, request, format=None):
        contacts = Contacts.objects.all()
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)   

    
class TaskAssignmentsView(APIView):
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]


    def get(self, request, format=None):
        taskassignments = TaskAssignments.objects.all()
        serializer = AssignmentSerializer(taskassignments, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []#(AllowAny,)
    serializer_class = RegisterSerializer
    
def registerPage(request): 
    print('kick register')        
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return HttpResponse("Answer")
   # return render(request,'login.html')
   # Redirect to a success page.
    
def createTodoView(request):   
    return render(request,'createTask.html')

def makeAssigments(ass, todo):    
    taskAssignments = TaskAssignments.objects.filter(todoitem = todo)
    serializer = AssignmentSerializer(taskAssignments, many = True)
    data = serializer.data
    for a in ass:
       if contain(data,a) ==False:
           print('ist created')
           contact = Contacts.objects.filter(pk = a['id'])
           TaskAssignments.objects.create(todoitem = todo,contact = contact[0])
       else:
           print('exist')

def contain(databaseAss,a):
    for dataAss in databaseAss:
        if dataAss['contact']['name']==a['name']:
            return True
    return False
    

def makeSubtask(subs, todo):    
    for s in subs:
        if s['id']=='null':
            print('call null make Subtask')
            sub = Subtask.objects.create(title=s['title'], checked = s['checked'])        
            sub.save()           
            ass = SubtasksList.objects.create(subtask= sub,todoitem = todo)
            ass.save()                
   

class editTodoViewAPI(generics.CreateAPIView):
    print('call createTodoViewAPI')  
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]
    #todo = TodoItem.objects.create(title = 'Test1',description="test1",date=date.today(),category='Sales',color='#ab234',checked=False,prio='1',state ='1')
    queryset = TodoItem.objects.all()
    permission_classes = []
    serializer_class = TodoItemSerializer  
    # Create wird automatisch bei POST aufgerufen
    def create(self, request):
         print('call edit')
         # wichtig in request.POST.get('title') sind nur Information gespeichert, die mit einem Form gepostet wurden 
         data = json.loads(request.body)  
         id = data['id']  
         todo = TodoItem.objects.filter(pk = id)[0]
         todo.title = data['title']
         todo.description = data['description']
         todo.date = data['date']
         todo.category = data['category']
         todo.prio = data['prio']
         todo.state = data['state']
        # print(data)
         makeSubtask(data['subtask'],todo)
         makeAssigments(data['assignments'],todo)
         todo.save()
        # serializer = TodoItemSerializer(todo, many=False)     
         #return Response(serializer.data)
         return Response('ok')
     

            

class createTodoViewAPI(generics.CreateAPIView):
    print('call createTodoViewAPI')  
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]
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
         setAssignmentandSubs(todoData)
         return Response(serializer.data)
    # Wird autimatisch bei GET aufgerufen  
    def get(self, request, format=None):
        todos = TodoItem.objects.all()       
        serializer = TodoItemSerializer(todos, many=True)       
        todoData = serializer.data
        for t in todoData:          
            setAssignmentandSubs(t)              
        return Response(serializer.data) 

def setAssignmentandSubs(t):
     print('call setAssignmentandSubs')
     if t['assignments'] !=[]:
                x = len(t['assignments'])
                for i in range(0, x):
                   id = t['assignments'][i]                  
                  # t['assignments'][i] = getContactsbyId(id) 
                   t['assignments'][i] = { 'id':id ,'name': getContactsbyId(id)} 
     if t['subtask'] !=[]:
                x = len(t['subtask'])
                for i in range(0, x):
                   id = t['subtask'][i] 
                   s = getSubtaskbyId(id) 
                   print(s)           
                   t['subtask'][i] = {'id':id, 'title': s['title'],'checked': s['checked'] } 
