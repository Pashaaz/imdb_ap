from django.contrib.auth.backends import BaseBackend


# creating my custom authentication backend and its credentials
class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        pass
