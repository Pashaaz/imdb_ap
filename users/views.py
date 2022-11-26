from django.core.cache import *
from django.contrib.auth.backends import BaseBackend
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, CreationForm
from django.contrib.auth import login, logout, authenticate

'''Login view
it does the job of using a username and password for user login
when login(request) is called, a session is created for the user'''
# class LoginBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         pass


def user_login(request):
    if request.user.is_anonymous:
        if request.method == "GET":
            cache.set('next', request.GET.get('next', None))
            form = LoginForm()
            return render(request, 'users/login.html', context={'form': form})
        elif request.method == "POST":
            user = authenticate(request, email=request.POST.get('email'),
                                password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    return HttpResponseRedirect(next_url)

                return redirect('movies_list')
            else:
                form = LoginForm()
                return render(request, 'users/login.html', context={'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('movies_list')


def user_signup(request):
    if request.user.is_anonymous:
        if request.method == "GET":
            signup_form = CreationForm()
            return render(request, 'users/signup.html',
                          context={'form': signup_form})
        elif request.method == "POST":
            form = CreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.warning(
                    request,
                    "Sorry! This email is taken."
                )
                messages.success(
                    request,
                    "Signup Success!"
                )
                return redirect('user_login')
            else:
                return redirect('user_signup')
