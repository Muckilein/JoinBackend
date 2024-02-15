"""
URL configuration for joinbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from todolist.views import TodoViewSet
from todolist.views import TodoItemsView
from todolist.views import LoginView
from todolist.views import ContactsView,TaskAssignmentsView,RegisterView,createTodoViewAPI,registerPage,logout_view,createTodoView

router = routers.DefaultRouter()
router.register(r'todo', TodoViewSet)
#router.register(r'login', LoginView.as_view())

urlpatterns = [
    path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('todos/', TodoItemsView.as_view()),
    path('contacts/', ContactsView.as_view()),
    path('assign/', TaskAssignmentsView.as_view()),
    path('registerAPI/', RegisterView.as_view(), name='auth_register'),
    path('register/', registerPage),  #only for testing  is replaced by frontend
    path('logout/', logout_view),
    path('createTodo/', createTodoView), # only for testing  is replaced by frontend
    path('createTodoAPI/', createTodoViewAPI.as_view())   
]
