
from .serializers import AssignmentSerializer,ContactsNameSerializer,SubtasksSerializer,CategorySerializer,SubtasksListSerializer#,ContactAssigmentSerializer
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList,Category

from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

"""
If a given user is not already in the assignment list a new assignments for the given todo is created.
"""
def makeAssigments(ass, todo):    
    taskAssignments = TaskAssignments.objects.filter(todoitem = todo)
    serializer = AssignmentSerializer(taskAssignments, many = True)
    data = serializer.data
    print("pint data")
    print(data)
    print(ass)
    for a in ass:
       if contain(data,a) ==False:
           print('ist created')
           contact = Contacts.objects.filter(pk = a['id'])
           TaskAssignments.objects.create(todoitem = todo,contact = contact[0])
       else:
           print('exist')
           
"""
returns wheather or not a given user is already in the assignment list of a task
"""
def contain(databaseAss,a):
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

"""
Deletes all assignments that are no longer assigned to the given todo
"""
def deleteAssigment(ass,todo):
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

def containSub(DBa,subss):
    print("DBA")
    print(DBa)
    print(subss)
    for a in subss:      
        if a['id']== DBa['subtask']:
           return True
    return False  
 
"""
Deletes all assignments that are no longer assigned to the given todo
"""
def deleteSubtask(subss,todo):
    subtask = SubtasksList.objects.filter(todoitem = todo)
    serializer = SubtasksListSerializer(subtask, many = True)
    databaseSubs = serializer.data   
    i=-1
    for dataSubs in databaseSubs:
        i=i+1
        if not containSub(dataSubs,subss):                 
           task= subtask[i]
           task.delete()


       
    
"""
Creates new subtasks with the information stored in subs.
Creates new objects that stores that links the previously created subtask to the given task 
"""
def makeSubtask(subs, todo):    
    for s in subs:
        if s['id']=='null':          
            sub = Subtask.objects.create(title=s['title'], checked = s['checked'])        
            sub.save()           
            ass = SubtasksList.objects.create(todoitem = todo,subtask = sub)
            subbis = SubtasksList.objects.create(todoitem = todo,subtask = sub)
            print('SubtasksList new Object')
            print(ass)
            print('Save subtask')
            subbis.subtask = sub
            subbis.save()
            ass.save()
        else:          
            su =  Subtask.objects.filter(pk = s['id'])[0]
            su.checked =  s['checked'] 
            su.save() 
       
                                    
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
                   
def setCategory(d):
    print(d['category'])
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
    

# def getSerializedContactsOfUsers(contacts,bool):
#     serializer = ContactAssigmentSerializer(contacts, many=bool)       
#     contactData = serializer.data  
#     list =[]
#     for c in contactData:
#         list.append(c['contacts']['id'])
#     return {'list':list} 
    


#Blog.objects.filter(pk__in=[1, 4, 7])