from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

#import django authentication functions
from django.contrib.auth import authenticate, login, logout
#importing the models from models.py
from .models import User, Todo
#importing the serializer classes
from .serializers import UserSerializer, TodoSerializer
from rest_framework.permissions import IsAuthenticated



# Create your views here.

def index(request):
    # if user is not authenticated redirect to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request,"todo/index.html")




##view for registering the user
def register(request):
    #if any user is already signed in redirect to index page
    if request.user.is_authenticated:
        return  HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        #Get the details from user submitted form for creating a new user
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST["confirmation"]

        #If passwords don't match through Error message
        if password!=confirmation:
            return render(request, "todo/register.html",{
                "message":"Passwords must match"
                })
        #Attempt to create new User
        try:
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
        except IntegrityError:
            return render(request, "todo/register.html",{
                "message":"Email already taken"
            })
        return HttpResponseRedirect(reverse('login'))
    return render(request, "todo/register.html")


##view for logging in the user
def login_view(request):
    #if user already exists redirect to index page
    if request.user.is_authenticated:
        return  HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        #authenticate the user with provided credentails
        user = authenticate(request,email=email,password=password)
        #if user exits with given credentails redirect to index view
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        #else through error message
        else:
            return render(request, "todo/login.htnl",{
                "message":"Invalid Credentails"
            })
    return render(request, "todo/login.html")



#defining the api_view endi points
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def todos(request):
    if not request.user.is_authenticated:
        return Response("you are not logged in")
    #if method is GET return all todos that correspond to a logged in user
    if request.method == "GET":
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    # if method is POST which here is for User trying to create a new todo
    elif request.method=="POST":
        body = request.data['body']
        user = request.user
        todo = Todo.objects.create(user=user, body=body)
        serializer = TodoSerializer(todo, many=False)
        return Response(serializer.data)



#dealing with deleting or modifying a particular todo by its primary key
@api_view(['PATCH','DELETE'])
def modifytodo(request,pk):
    #if request metod is delete then go ahead and delete the todo
    if request.method=="DELETE":
        try:
            todo = Todo.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {"Error":"no such models exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        todo.delete()
        return Response("deleted")
    # if requesting method is PATCH go ahead and modify the post
    elif request.method == "PATCH":
        status = request.data['completed']
        try:
            todo = Todo.objects.get(pk=pk)
        except ObjectDoesNotExist:
            content = {"Error":"no such models exist"}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        todo.completed = status
        todo.save()
        serializer = TodoSerializer(todo,many=False)
        return Response(serializer.data)




def logout_view(request):
    #logout the user by clearing the session data
    logout(request)
    return HttpResponseRedirect(reverse('login'))