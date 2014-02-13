import datetime
from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length = 140)
    user = models.ForeignKey(User)
    priority = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length = 140)
    board = models.ForeignKey(Board)
    priority = models.IntegerField(default = 0)
    completed = models.BooleanField(default = False)

    def __unicode__(self):
        return self.name

#forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 140)
    password = forms.CharField(max_length = 140)

class BoardForm(forms.Form):
    name = forms.CharField(max_length = 140)

class TaskForm(forms.Form):
    name = forms.CharField(max_length = 140)

class UserForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    password_confirm = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)