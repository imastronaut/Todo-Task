from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth import authenticate, login, logout
from .models import User, Todo
from .serializers import UserSerializer, TodoSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated



# Create your views here.

def index(request):
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



@api_view(['GET','POST'])
def todos(request):
    if not request.user.is_authenticated:
        return Response("you are not logged in")
    if request.method == "GET":
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    if request.method=="POST":
        body = request.data['body']
        user = request.user
        todo = Todo.objects.create(user=user, body=body)
        serializer = TodoSerializer(todo, many=False)
        return Response(serializer.data)

@api_view(['PATCH','DELETE'])
def modifytodo(request,pk):
    if request.method=="DELETE":
        todo = Todo.objects.get(pk=pk)
        todo.delete()
        return Response("deleted")
    elif request.method == "PATCH":
        status = request.data['completed']
        todo = Todo.objects.get(pk=pk)
        todo.completed = status
        todo.save()
        serializer = TodoSerializer(todo,many=False)
        return Response(serializer.data)







def logout_view(request):
    #logout the user by clearing the session data
    logout(request)
    return HttpResponseRedirect(reverse('login'))