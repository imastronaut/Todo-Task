from rest_framework.serializers import ModelSerializer

from .models import User, Todo

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']

class TodoSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Todo
        fields = "__all__"