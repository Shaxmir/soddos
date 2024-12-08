from dataclasses import dataclass
from datetime import datetime
from http.client import responses

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserAuthenticationForm
# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сначала создаём объект, но не сохраняем в базу
            user.is_superuser = False  # Указываем, что пользователь не является суперпользователем
            user.is_staff = False
            user.is_active = True
            user.date_joined = datetime.now()
            user.save()  # Теперь сохраняем изменения в базу данных
            login(request, user)

            response = redirect('/')  # Редирект на главную страницу после входа
            max_age_cookie = 60 * 60 * 24 * 30  # Время жизни куки 30 дней
            response.set_cookie('user_id', user.id, max_age=max_age_cookie)  # Сохраняем кукисы
            return response
    else:
        form = UserRegistrationForm()
    return render(request, 'saccount/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)

                #Сохраняем данные в куки
                response = redirect('/')#Редирект на главную страницу после входа
                max_age_cookie = 60 * 60 * 24 * 30#Время жизни куки 30 дней
                response.set_cookie('user_id', user.id, max_age=max_age_cookie)#Сохраняем кукисы
                return response
    else:
        form = UserAuthenticationForm()
    return render(request, 'saccount/login.html', {'form': form})

def logout_view(request):
    logout(request)

    #Удаляем куки
    response = redirect('/')
    response.delete_cookie('user_id')
    return  response