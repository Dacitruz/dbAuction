from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from .forms import ProfileForm


def sign_up(request):
    data = dict()
    if request.method == 'GET':
        data['title'] = 'Регистрация'
        return render(request, 'accounts/sign_up.html', context=data)
    elif request.method == 'POST':
        # Извлечение данных из формы:
        login_x = request.POST.get('login')
        pass1_x = request.POST.get('pass1')
        pass2_x = request.POST.get('pass2')
        email_x = request.POST.get('email')
        # Каскад проверок данных (валидация):
        if pass1_x != pass2_x:
            data['color_x'] = 'red'
            data['report_x'] = 'Пароли на совпадают!'
        elif pass1_x == '':
            data['color_x'] = 'red'
            data['report_x'] = 'Парольне может быть таким!'
        elif User.objects.filter(email__iexact=email_x).exists():
            data['color_x'] = 'red'
            data['report_x'] = 'Email Занят'
        elif User.objects.filter(username__iexact=login_x).exists():
            data['color_x'] = 'red'
            data['report_x'] = 'Login Занят'
        else:
            # Техническая проверка:
            data['login'] = login_x
            data['pass1'] = pass1_x
            data['pass2'] = pass2_x
            data['email'] = email_x
            # Добавление пользователя в БД:
            user = User.objects.create_user(login_x, email_x, pass1_x)
            user.save()
            # Формирование отчета:
            data['title'] = 'Отчет о регистрации'
            if user is None:
                data['color_x'] = 'red'
                data['report_x'] = 'В регистрации отказано!'
            else:
                data['color_x'] = 'green'
                data['report_x'] = 'Регистрация успешно завершена!'
        return render(request, 'accounts/reports.html', context=data)


def sign_in(request):
    data = dict()
    if request.method == 'GET':
        data['title'] = 'Авторизация'
        return render(request, 'accounts/sign_in.html', context=data)
    elif request.method == 'POST':
        # Получение данных:
        login_x = request.POST.get('login')
        pass1_x = request.POST.get('pass1')
        # Проверка подлинности:
        user = authenticate(request, username=login_x, password=pass1_x)
        if user is None:
            data['color_x'] = 'red'
            data['report_x'] = 'Пользоавтель не найден!'
            data['title'] = 'Отчет об авторизации'
            return render(request, 'accounts/reports.html', context=data)
        else:
            login(request, user)
            return redirect('/home')


def sign_out(request):
    logout(request)
    return redirect('/home')

def edit_profile(request):
    data = dict()
    if request.method == 'GET':
        data['title'] = 'Авторизация'
        return render(request, 'accounts/profile.html', context=data)
    else:
        return redirect('/home')
# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('/home')
#         else:
#             return redirect('/home')
#     else:
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'accounts/profile.html', {
#         'profile_form': profile_form
#     }