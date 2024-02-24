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
from django.views.generic.detail import DetailView

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TodoItem.objects.all() #.order_by('date')
    serializer_class = TodoItemSerializer

"""
Returns the name of a contscts with the given id
"""       
def getContactsbyId(id):
    contact = Contacts.objects.all()
    serializerContact = ContactsNameSerializer(contact, many=True)
    contactData = serializerContact.data
    for c in  contactData:
        if c['id']==id:
          return c['name'] 
    return ''  

"""
returns a JSON containing the title and checked-state of a given subtask
"""
def getSubtaskbyId(id):
    subs = Subtask.objects.filter(pk = id)
    subSerilizer =  SubtasksSerializer(subs,many=True)      
    s = subSerilizer.data[0]
    return {'title':s['title'] , 'checked': s['checked']}         
       
   
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

    
# class TaskAssignmentsView(APIView):
#     authentication_classes =[TokenAuthentication]
#     permission_classes =[IsAuthenticated]


#     def get(self, request, format=None):
#         taskassignments = TaskAssignments.objects.all()
#         serializer = AssignmentSerializer(taskassignments, many=True)
#         return Response(serializer.data)

"""
Registers a User when the given data are correct
"""
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []
    serializer_class = RegisterSerializer

# """
# Renders the register page
# """
# def registerPage(request):          
#     return render(request,'register.html')

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
If a given user is not already in the assignment list a new assignments for the given todo is created
"""
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
"""
returns wheather or not a given user is already in the assignment list if a titi
"""
def contain(databaseAss,a):
    for dataAss in databaseAss:
        if dataAss['contact']['name']==a['name']:
            return True
    return False
    
"""
Creates new subtasks with the information stored in subs.
Creates new objects that stores that links the previously created subtask to the given task 
"""
def makeSubtask(subs, todo):    
    for s in subs:
        if s['id']=='null':
            print('call null make Subtask')
            sub = Subtask.objects.create(title=s['title'], checked = s['checked'])        
            sub.save()           
            ass = SubtasksList.objects.create(subtask= sub,todoitem = todo)
            ass.save()
        else:
            print("id is")
            print(s['id'])
            su =  Subtask.objects.filter(pk = s['id'])[0]
            su.checked =  s['checked'] 
            su.save()
                           
   


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
Edits the inforamtion of assigments in the way, that not only the id of the user is given but also the name.
Edits the inforamtion the subtasks in the way, that not only the id of the subtask is given, but alo the title and wheather it is checked or not
"""   
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
                   t['subtask'][i] = {'id':id, 'title': s['title'],'checked': s['checked'] } 
                   
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
 
