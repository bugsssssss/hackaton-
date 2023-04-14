from django import forms
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
        fields = ['username', 'email', 'password1',
                  'password2']


class UserEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=[
        '%Y/%m/%d', '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y'], widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'Дата рождения'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name',
                  'last_name', 'phone_number1', 'phone_number2', 'skills', 'country', 'city', 'about', 'languages', 'education', 'skills', 'date_of_birth', 'personal_info']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'phone_number1': forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
            'phone_number2': forms.TextInput(attrs={'placeholder': 'Номер телефона'}),

            'country': forms.TextInput(attrs={'placeholder': 'Страна'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
        }


class OrderFeedbackForm(forms.ModelForm):
    class Meta:
        model = OrderFeedback
        fields = ['feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'placeholder': 'Оставьте отзыв'}),
        }


class OrderForm(forms.ModelForm):
    deadline = forms.DateField(input_formats=[
        '%Y/%m/%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y', '%d.%m.%y'])

    def clean_deadline_field(self):
        # Get the value of the field
        value = self.cleaned_data['deadline']

        # Your custom validation logic goes here
        if value.year < 2000:
            raise forms.ValidationError("Date must be after the year 2000")

        # Always return the cleaned value
        return value

    class Meta:
        model = Order
        fields = ['title', 'description', 'category',
                  'deadline', 'country', 'city', 'category', 'required_skills', 'budget', 'budget_type', 'budget_currency', 'owner']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Название проекта'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание проекта'}),
            'category': forms.Select(attrs={'placeholder': 'Категория'}),
            'budget': forms.NumberInput(attrs={'placeholder': 'Бюджет', 'calss': 'budget_input'}),
            'budget_type': forms.Select(attrs={'placeholder': 'Тип бюджета'}),
            'budget_currency': forms.Select(attrs={'placeholder': 'Валюта'}),
            'deadline': forms.DateInput(attrs={'placeholder': 'dd.mm.yyyy'}),
            'country': forms.TextInput(attrs={'placeholder': 'Страна'}),
            'city': forms.TextInput(attrs={'placeholder': 'Город'}),
            'required_skills': forms.TextInput(attrs={'placeholder': 'Требуемые навыки', 'class': 'skills_select'}),
            'owner': forms.Select(attrs={'placeholder': 'Владелец'})
        }
