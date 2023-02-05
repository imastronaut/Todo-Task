from rest_framework.serializers import ModelSerializer

from .models import User, Todo

#define the serailizer class to serializer Model objects

#Defining user serializer 
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        #specifying the fields that are to be included in serialized object
        fields = ['id','username', 'email']

class TodoSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Todo
        #specifying that all fields are to be included in the serialized object
        fields = "__all__"