##Backend application for implementing the TODO list application using Django rest framework

This repository details the code for developing a backend for Todo List application

This Todo application allows user's to make list of todo and uses django's default authentication system



to run this project on your local machine first install requirement by typing the following to command line
```sh
pip install - r requriments.txt
```

Now you should have install all the requirements needed for this project

Go ahead and makemigrations, which is responsible for creating new migrations based on the changes you have made to your models.

```sh
python manage.py makemigrations
```
Now apply those changes to apply to your database by typing the following command

```sh
python manage.py migrate
```

You are now good to go 

start your local server by typing following command

```sh
python manage.py runserver
```




