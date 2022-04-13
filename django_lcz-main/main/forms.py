from django import forms
from matplotlib import widgets
from .models import Customer, Task
from django.forms import ModelForm, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

#личный кабинет
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
        widgets = {'profile_pic': forms.FileInput} #что бы убрать ненужное в поле загрузки

#создание карточки
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

#регистрация
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
