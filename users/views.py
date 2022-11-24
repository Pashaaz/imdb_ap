from django.contrib.auth.backends import BaseBackend
from django.shortcuts import render


# Login view
# it does the job of using a username and password for user login
# when login(request) is called, a session is created for the user
class LoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        pass
