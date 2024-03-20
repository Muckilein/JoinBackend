from django.db import models
from datetime import date
import datetime
#from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.models import AbstractUser,BaseUserManager
#Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
     email=models.CharField(max_length=100,unique=True)      
     iconColor=models.CharField(max_length=30,default="#9327FF")
     phone=models.CharField(max_length=30,default=' ',null=True)
     username=models.CharField(max_length=100,default=' ')
     short= models.CharField(max_length=30,default='u')
     #reg= models.BooleanField(default=False) 
    
     USERNAME_FIELD = "email"
     REQUIRED_FIELDS = []
     objects = CustomUserManager() 
     def __str__(self):        
        return  self.username    
     
               
class Contacts(models.Model):
     email=models.CharField(max_length=100,default = "User@mail")      
     iconColor=models.CharField(max_length=30,default="#9327FF")
     phone=models.CharField(max_length=30,default=' ',null=True)
     username=models.CharField(max_length=100,default='user')
     short= models.CharField(max_length=30,default='u')
     #reg= models.BooleanField(default=False)  
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)   
     
     def __str__(self):
          #return self.email + " "+  self.name  + " "+ self.iconColor +self.phone + " "+ self.short
        return  self.username  
             
class Subtask(models.Model):
     checked = models.BooleanField(default= False)
     title = models.CharField(max_length=30,default='Subtask')
     
     def __str__(self):
        return self.title
     
class Category(models.Model):     
     title = models.CharField(max_length=50,default='')
     color = models.CharField(max_length=50,default='',null=True)
     
     def __str__(self):
        return self.title
     
# class ContactsUser(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)   
#    contacts = models.ForeignKey(Contacts, on_delete=models.CASCADE, null=True)
   
#    def __str__(self):
#         return (self.user.username + self.contacts.name)

class TodoItem(models.Model):
   title = models.CharField(max_length=100,default='')
   description = models.CharField(max_length=1000,default='')
   date = models.DateField(default=datetime.date.today)
   assignments = models.ManyToManyField(User,through='TaskAssignments') #Many-to-Many
   subtask = models.ManyToManyField(Subtask,through='SubtasksList') #Many-to-Many
   #category = models.CharField(max_length=30,default='')
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   color=models.CharField(max_length=30,default='')
   checked = models.BooleanField(default=False)
   prio = models.CharField(max_length=30,default='')
   state = models.CharField(max_length=30,default='')
   
   def __str__(self):
        return self.title

class TaskAssignments(models.Model):
   todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   
   def __str__(self):
       return self.user.username
   


class SubtasksList(models.Model):
   todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
   subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
   
   def __str__(self):
       return (self.subtask.title + " " +self.todoitem.title)

   
   

     