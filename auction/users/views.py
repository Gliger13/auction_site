from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from users.forms import RegistrationForm, LoginForm


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'users/register.html', context={"form": form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.get_user(request)
            print(user)
            if user:
                login(request, user)
                return render(request, 'users/register_success.html')
            else:
                return render(request, 'users/register.html', context={"form": form})
        else:
            return render(request, 'users/register.html', context={"form": form})


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', context={'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user(request)
            if user:
                login(request, user)
                return redirect('/')
            else:
                form.errors[NON_FIELD_ERRORS] = 'Cannot perform login with this credentials'
                return render(request, 'users/login.html', context={'form': form})
        else:
            return render(request, 'users/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('')
