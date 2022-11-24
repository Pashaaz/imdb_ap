from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


# Register your models here.
# Created classes should also be added here, based on models

admin.site.register(User, UserAdmin)
