from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import NON_FIELD_ERRORS
from django.http import HttpResponseRedirect, Http404
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
            user.send_verification_email()
            if user:
                login(request, user)
                return render(request, 'users/register_success.html')
            else:
                return render(request, 'users/register.html', context={"form": form})
        else:
            return render(request, 'users/register.html', context={"form": form})


def verify(request):
    user = request.user
    data = request.GET
    if user.is_token_correct(data['token']):
        user.verify_email()
        return render(request, 'users/email_verified.html')
    else:
        return Http404("Not Found")


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
