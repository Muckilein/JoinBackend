from django.db import models
from datetime import date
import datetime
#from django.contrib.auth.models import User
from django.conf import settings 
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

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
   assignments = models.ManyToManyField(Contacts,through='TaskAssignments') #Many-to-Many
   subtask = models.ManyToManyField(Subtask,through='SubtasksList') #Many-to-Many
   #category = models.CharField(max_length=30,default='')
   category = models.ForeignKey(Category, on_delete=models.CASCADE)
   color=models.CharField(max_length=30,default='')   
   prio = models.CharField(max_length=30,default='')
   state = models.CharField(max_length=30,default='')
   userTodo = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='userTodo')
   
   def __str__(self):
        return self.title

class TaskAssignments(models.Model):
   todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
   contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
   
   def __str__(self):
       return self.contact.username
   


class SubtasksList(models.Model):
   todoitem = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
   subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
   
   def __str__(self):
       return (self.subtask.title + " " +self.todoitem.title)




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # 'reset_password_url': "{}?token={}".format(
        #     instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        #     reset_password_token.key)
        #  'reset_password_url': "http://127.0.0.1:5500/html/reset-your-password.html?path={}&token={}".format(
        #   instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
        #   reset_password_token.key)
          'reset_password_url': "http://join.julia-developer.de/Join-frontend/html/reset-your-password.html?path={}&token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }
    print(context)

    # render email text 
    email_html_message = render_to_string('user_reset_password.html', context)
    email_plaintext_message = render_to_string('user_reset_password.txt', context)
    print(email_html_message)
    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
   
   

     