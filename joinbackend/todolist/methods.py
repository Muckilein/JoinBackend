
from .serializers import AssignmentSerializer,ContactsNameSerializer,SubtasksSerializer,CategorySerializer
from .models import TodoItem,Contacts,TaskAssignments,Subtask,SubtasksList,Category
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
            #print('call null make Subtask')
            sub = Subtask.objects.create(title=s['title'], checked = s['checked'])        
            sub.save()           
            ass = SubtasksList.objects.create(subtask= sub,todoitem = todo)
            ass.save()
        else:
            #print("id is")
            #print(s['id'])
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
    
                   