from django import forms
from matplotlib import widgets
from .models import Task
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"] #как в models
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Введите слово'
        }),
            "task": TextInput(attrs={
                'class': 'form-control',
                'placeholder' : 'Введите перевод'
        }),
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
