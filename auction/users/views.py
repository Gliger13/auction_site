from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from users.forms import RegistrationForm


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'users/register.html', context={"form": form})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return render(request, 'users/register_success.html')
        else:
            return render(request, 'users/register.html', context={"form": form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('')
