from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm, CustomUserCreationForm
from django.contrib.auth.models import User
from .models import *


def index(request):
    context = {
        'heading': 'Test page'
    }
    return render(request, 'index.html', context)


def profile(request):
    context = {
        'heading': 'Profile page'
    }
    return render(request, 'test.html', context)


def login_user(request):
    if request.POST:
        # email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {'form': UserForm,
                       'error': 'Неверный логин или пароль'}
            return render(request, 'enter.html', context)
    context = {'form': UserForm}

    return render(request, 'enter.html', context)


def register(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() and ('offer' in request.POST):
            user = form.save(commit=False)
            email = request.POST['email']
            already_exists = CustomUser.objects.filter(email=email).exists()
            if not already_exists:
                user.save()
                user = authenticate(
                    request, username=request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return redirect('index')
            else:
                context = {
                    'form': form,
                    'email_error': 'Такой email уже зарегистрирован',
                }
                return render(request, 'registration.html', context)
        else:
            context = {
                'form': form,
                'offer_error': 'Подтвердите согласие с правилами',
            }
            return render(request, 'registration.html', context)
    context = {'form': form}
    return render(request, 'registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')
