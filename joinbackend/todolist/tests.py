from django.test import TestCase
from django.test import Client
import unittest
from django.contrib.auth.models import User
from datetime import datetime  
from .models import TodoItem

# Create your tests here.
class JoinTest(TestCase):
    def test_makeclient(self):        
        self.client = Client()        
        # self.user = User.objects.create_user('test_user', password='test_user')
        self.user = User.objects.create( username='munni', email='Munni@mail.de',  first_name='Munni', last_name='Hase',password='111abcdefgh')        
        self.client.login(username='munni', password='111abcdefgh')       
        response = self.client.get('/createTodoAPI/') 
        print(self.user)       
        self.assertEqual(response.status_code, 200)
        pass
    
    def test_makeTodo(self):       
                
        # self.user = User.objects.create_user('test_user', password='test_user')
        todo = TodoItem.objects.create(title = 'Schreiben',description='Schreiben eine Mail!',date=datetime.now,category= 'sale',color= '#ffffff',checked=False,prio= '1',state = '1')        
        self.client.login(username='munni', password='111abcdefgh')       
        response = self.client.get('/createTodoAPI/') 
        print(self.user)       
        self.assertEqual(response.status_code, 200)
        pass
