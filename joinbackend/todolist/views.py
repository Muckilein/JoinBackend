from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import viewsets
from .models import TodoItem
from .serializers import TodoSerializer
from django.core import serializers
from django.http import HttpResponse
from .models import Contacts

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TodoItem.objects.all() #.order_by('date')
    serializer_class = TodoSerializer
    permission_classes =[]# [permissions.IsAuthenticated]
    
    def create(self,request):
       todo = TodoItem.objects.create(title= request.POST.get('title', ''), 
                                  description= request.POST.get('description', ''),
                                  user= request.user,
                                )
       serialized_obj = serializers.serialize('json', [todo, ]) 
       return HttpResponse(serialized_obj, content_type='application/json')

def ContactsView(request):
  contact,created = Contacts.objects.get_or_create(email='Maria@mail.com',iconColor='#ee27FF',phone='', name='Maria Müller',short= 'MM') 
  #task,created = Contacts.objects.get_or_create(email='Maria@mail.com',iconColor='#ee27FF',phone='', name='Maria Müller',short= 'MM') 
  print("call ContactsView")
  if created:
     print('exist')  
  return render(request,'index.html',{'contact':contact})