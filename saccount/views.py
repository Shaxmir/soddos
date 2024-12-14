from dataclasses import dataclass
from datetime import datetime
from http.client import responses
from axes.utils import get_client_ip_address
from axes.models import AccessAttempt
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserAuthenticationForm, ProfileImgForm
from .models import ProfileImg


# Create your views here.

def profile(request):
    prof = get_object_or_404(User, id=request.user.id)
    avatar = request.user
    return render(request, 'saccount/profile.html', context={'prof': prof, 'avatar': avatar})

def register_view(request):
    is_locked = False
    client_ip = get_client_ip_address(request)

    if client_ip:
        attempt = AccessAttempt.objects.filter(ip_address=client_ip).last()
        if attempt and attempt.failures_since_start >= 5:  # Проверяем лимит неудачных попыток
            is_locked = True

    if is_locked:
        return render(request, 'saccount/register.html', {'is_locked': True})  # Передаем флаг блокировки
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сначала создаём объект, но не сохраняем в базу
            user.is_superuser = False  # Указываем, что пользователь не является суперпользователем
            user.is_staff = False
            user.is_active = True
            user.date_joined = datetime.now()
            user.save()  # Теперь сохраняем изменения в базу данных
            user = authenticate(
                request=request,  # Передаем request
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                backend='axes.backends.AxesBackend'  # Указываем конкретный backend
            )

            if user is not None:
                login(request, user)  # Выполняем вход
                return redirect('/')  # Редирект на главную страницу
            else:
                form.add_error(None, 'Неправильный логин или пароль')
        else:
        # Если форма не валидна, возвращаем тот же шаблон с ошибками
            return render(request, 'saccount/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'saccount/register.html', {'form': form})

def login_view(request):
    # Логика для проверки блокировки
    is_locked = False
    client_ip = get_client_ip_address(request)  # Получаем IP пользователя
    username = request.POST.get('username', '')

    # Проверка блокировки по IP или имени пользователя
    if client_ip:
        attempts = AccessAttempt.objects.filter(ip_address=client_ip).last()
        if attempts and attempts.failures_since_start >= 5:  # Лимит попыток входа
            is_locked = True

    if username and not is_locked:
        attempts = AccessAttempt.objects.filter(username=username).last()
        if attempts and attempts.failures_since_start >= 5:  # Лимит попыток входа
            is_locked = True

    # Если аккаунт заблокирован, передаём сообщение об ошибке
    if is_locked:
        return render(request, 'saccount/login.html', {
            'form': UserAuthenticationForm(),
            'is_locked': True,
        })

    # Если аккаунт не заблокирован, продолжаем стандартную обработку
    if request.method == 'POST':
        form = UserAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request=request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Неправильный логин или пароль')
        else:
            form.add_error(None, 'Некорректные данные для входа')
    else:
        form = UserAuthenticationForm()

    return render(request, 'saccount/login.html', {'form': form, 'is_locked': False})

def logout_view(request):
    logout(request)

    #Удаляем куки

    return  redirect('/')

def edit_profile(request):
    profile = request.user.profile_img
    if request.method == 'POST':
        form = ProfileImgForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/saccount/profile/')
    else:
        form = ProfileImgForm(instance=profile)
    return render(request, 'saccount/edit_profile.html', {'form': form})