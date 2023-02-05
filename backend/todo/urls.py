from django.urls import path

from . import views


#define the url patterns
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("todos/",views.todos, name="todos"),
    path("todo/<str:pk>", views.modifytodo, name="modify")
]