
from .serializers import AssignmentSerializer,ContactsSerializer,SubtasksSerializer,CategorySerializer,SubtasksListSerializer#,ContactAssigmentSerializer
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList,Category,User

from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model


def makeAssigments(ass, todo):
    """
    If a given user is not already in the assignment list a new assignments for the given todo is created.
    """    
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
    """
    returns wheather or not a given user is already in the assignment list of a task
    """
    for dataAss in databaseAss:
        if dataAss['contact']['id']==a['id']:
            print('true')            
            return True    
    print('false')
    return False

def contain2(DBa,ass):
    for a in ass:
        if a['id']== DBa['contact']['id'] :
           return True
    return False


def deleteAssigment(ass,todo):
    """
    Deletes all assignments that are no longer assigned to the given todo
    """
    taskAssignments = TaskAssignments.objects.filter(todoitem = todo)
    serializer = AssignmentSerializer(taskAssignments, many = True)
    databaseAss = serializer.data
    i=-1
    for dataAss in databaseAss:
        i=i+1
        if not contain2(dataAss,ass): 
           print('delete',taskAssignments[i])         
           taskAss = taskAssignments[i]
           taskAss.delete()

   
    

def makeSubtask(subs, todo):
    """
    Creates new subtasks with the information stored in subs.
    reates new objects that stores that links the previously created subtask to the given task 
    """      
      
    for s in subs:
        if s['id']=='null':                  
            obj = Subtask.objects.filter (title = s['title'])             
            if len(obj) ==0:               
                sub = Subtask.objects.create(title=s['title'], checked = s['checked'])              
                todo.subtask.add(sub)
            else:                              
             sub= Subtask.objects.filter(title = obj[0].title)[0]            
             todo.subtask.add(sub)        
        else:         
            su =  Subtask.objects.filter(pk = s['id'])[0]
            su.checked =  s['checked'] 
            su.save()
        todo.save()  
       
                                    
     
def getContactsbyId(id):
    """
    Returns the name of a contscts with the given id
    """  
    contact = Contacts.objects.all()
    serializerContact = ContactsSerializer(contact, many=True)
    userData = serializerContact.data
    for u in  userData:
        if u['id']==id:
          return u['username'] 
    return ''  


def getSubtaskbyId(id):
    """
    returns a JSON containing the title and checked-state of a given subtask
    """
    subs = Subtask.objects.filter(pk = id)
    subSerilizer =  SubtasksSerializer(subs,many=True)      
    s = subSerilizer.data[0]
    return {'title':s['title'] , 'checked': s['checked']}         
       

def setAssignmentandSubs(t):
     """
    Edits the inforamtion of assigments in the way, that not only the id of the user is given but also the name.
    Edits the inforamtion the subtasks in the way, that not only the id of the subtask is given, but alo the title and wheather it is checked or not
    """   
     if t['assignments'] !=[]:
                x = len(t['assignments'])
                for i in range(0, x):
                   id = t['assignments'][i]                
                   t['assignments'][i] = { 'id':id ,'name': getContactsbyId(id)} 
     if t['subtask'] !=[]:
                x = len(t['subtask'])
                for i in range(0, x):
                   id = t['subtask'][i] 
                   s = getSubtaskbyId(id)                             
                   t['subtask'][i] = {'id':id, 'title': s['title'],'checked': s['checked'] } 
                   
def setCategory(d):
    
    id = d['category']
    cat = Category.objects.filter(id = id)[0]
    # serializer = CategorySerializer(cat, many=False)       
    # categoryData = serializer.data 
    categoryData=getSerializedCategory(cat,False)
    category = {'id':id, 'title':categoryData['title']}
    d['category'] = category
    
def getSerializedCategory(category,bool):
    serializer = CategorySerializer(category, many=bool)       
    categoryData = serializer.data 
    return categoryData
    
