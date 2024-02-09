from django.db import models
from datetime import date
import datetime
from django.contrib.auth.models import User
from django.conf import settings 

#Create your models here.
# class UserModel(models.Model):
#      email=models.CharField(max_length=100,default = "User@mail")     
#      user = models.ForeignKey(User, on_delete=models.CASCADE)     
#      iconColor=models.CharField(max_length=30,default="#9327FF")
#      phone=models.CharField(max_length=30,default='')
#      name=models.CharField(max_length=100,default='user')
#      short= models.CharField(max_length=30,default='u')   
          
class Contacts(models.Model):
     email=models.CharField(max_length=100,default = "User@mail")      
     iconColor=models.CharField(max_length=30,default="#9327FF")
     phone=models.CharField(max_length=30,default=' ')
     name=models.CharField(max_length=100,default='user')
     short= models.CharField(max_length=30,default='u') 
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)   
     
     def __str__(self):
          #return self.email + " "+  self.name  + " "+ self.iconColor +self.phone + " "+ self.short
        return  self.name  
             
# class subtask(models.Model):
#      checked = models.BooleanField(default= False)
#      subtask = models.CharField(max_length=30,default='')

class TodoItem(models.Model):
   title = models.CharField(max_length=100,default='')
   description = models.CharField(max_length=1000,default='')
   date = models.DateField(default=datetime.date.today)
   assignments = models.ManyToManyField(Contacts,through='TaskAssignments')
#    subtask = models.ManyToManyField(subtask)
   category = models.CharField(max_length=30,default='')
   color=models.CharField(max_length=30,default='')
   #maxSubs = models.CharField(max_length=30,default='')
   checked = models.BooleanField(default=False)
   prio = models.CharField(max_length=30,default='')
   state = models.CharField(max_length=30,default='')
   
   def __str__(self):
        return self.title

class TaskAssignments(models.Model):
   todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
   contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
#    class Meta:
#         ordering = ["date"]

   
   

     