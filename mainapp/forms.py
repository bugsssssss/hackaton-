from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserForm(forms.ModelForm):
    # ? username
    username = forms.CharField(max_length=100)

    # email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            # 'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Логин'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        }


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'email '}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
