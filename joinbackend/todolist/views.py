from django.shortcuts import render ,redirect
from rest_framework import viewsets
from .models import TodoItem,Contacts,TaskAssignments
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import TodoItemSerializer,ContactsSerializer,AssignmentSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.http import HttpResponse

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TodoItem.objects.all() #.order_by('date')
    serializer_class = TodoItemSerializer

    
class TodoItemsView(APIView):
    authentication_classes =[TokenAuthentication]
    permission_classes =[IsAuthenticated]


    def get(self, request, format=None):
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)

class LoginView(ObtainAuthToken): 
   def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        
class ContactsView(APIView):
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]


    def get(self, request, format=None):
        contacts = Contacts.objects.all()
        serializer = ContactsSerializer(contacts, many=True)
        return Response(serializer.data)
    
    
class TaskAssignmentsView(APIView):
    authentication_classes =[]#[TokenAuthentication]
    permission_classes =[]#[IsAuthenticated]


    def get(self, request, format=None):
        taskassignments = TaskAssignments.objects.all()
        serializer = AssignmentSerializer(taskassignments, many=True)
        return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = []#(AllowAny,)
    serializer_class = RegisterSerializer
    
def registerPage(request): 
    print('kick register') 
    # form = UserCreationForm
    # context = { 'registerForm': form}     
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return HttpResponse("Answer")
   # return render(request,'login.html')
    # Redirect to a success page.