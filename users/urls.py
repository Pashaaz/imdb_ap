from django.urls import path
from .views import *

urlpatterns = [
    path('login', user_login, name='user_login'),
    path('signup', user_signup, name='user_signup'),
    path('logout', user_logout, name='user_logout')
]
