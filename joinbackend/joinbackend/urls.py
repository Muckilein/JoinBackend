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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from todolist.views import LoginView
from todolist.views import GuestExist,ContactsView,RegisterView,createTodoViewAPI,Logout_view,createTodoViewAPIDetail,categoryAPI,categoryAPIDetail,User_viewAPI,User_viewAPIDetail#,contactofUser

#router = routers.DefaultRouter()
#router.register(r'todo', TodoViewSet)
#router.register(r'login', LoginView.as_view())

urlpatterns = [
    #path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')), 
    
    path('contacts/<int:pk>/', ContactsView.as_view()),
    path('user/<int:pk>/', User_viewAPIDetail.as_view()),
    path('users/', User_viewAPI.as_view()), 
    path('guest/', GuestExist.as_view()),
    path('registerAPI/', RegisterView.as_view(), name='auth_register'),
    path('logout/', Logout_view.as_view()),
    path('createTodoAPI/', createTodoViewAPI.as_view()) ,    
    path('createTodoAPI/<int:pk>/', createTodoViewAPIDetail.as_view()) ,  
    path('categoryAPI/', categoryAPI.as_view()) ,  
    path('categoryAPI/<int:pk>/', categoryAPIDetail.as_view()) ,
    #path('reset_password/', auth_views.PasswordResetView.as_view(template_name ="reset.html"),name='reset_password'), # delete
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),name='reset_password'),    
    # path('reset_password_sent/',  auth_views.PasswordResetDoneView.as_view(template_name ="reset_password_sent.html"),name ='password_reset_done'),
    # path('reset_password/<uidb64>/<token>/',  auth_views.PasswordResetConfirmView.as_view(template_name ="reset.html"),name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),name='password_reset_complete'),
   
    
 
]
