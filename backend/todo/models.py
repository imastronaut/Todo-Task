from django.db import models

from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.


#Creating a custom user model for our project to make use of email for authentication rather than username
#First we have to add Auth_USER_MODEL setting to out project settings to use our App's custom User model for authentication

class User(AbstractUser):
    username = models.CharField(max_length=60)
    email = models.EmailField(max_length=60, unique=True)

    #Configure the username field that the appication asks for authentication to email
    USERNAME_FIELD = 'email'

    #Specify the fields that application promt the user other than username field(email here) and password

    REQUIRED_FIELDS = ['username']

    #Specify the manager class for our user model
    objects = CustomUserManager()

    #Specifying the string representation of UserModel
    def __str__(self):
        return self.email


#create a Todo Model to store user todos
class Todo(models.Model):

    #Create a foreignKey to refernce this particular todo to a user
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="todos")

    #TextField to store todo
    body = models.TextField()

    #Field to store timestamp when the todo was created
    createdAt = models.DateTimeField(auto_now_add=True)

    # A field to identify if the todo is completed or not
    completed = models.BooleanField(default=False)

    #Order the table based on lasted added todo
    class Meta:
        ordering = ['createdAt']

    #specifying the string representation of our todo model
    def __str__(self):
        return  self.body


