from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
# from django.core.validators import RegexValidator

# abstracting user model from AbstractUser (method 2)
''' 
class User(AbstractUser):
    phone_number = models.PositiveBigIntegerField(unique=True, validators=[
        RegexValidator(r'^989[0-3,9]\d{8}$', 'Enter a valid phone number.', 'invalid')])
    address = models.TextField(blank=True)
    birthday = models.DateField(null=True)
    avatar = models.ImageField(blank=True)
 
    # the 3 fields below are mentioned in Django's AbstractUser
    EMAIL_FIELD = "email"  # defines what field is specified for email
    USERNAME_FIELD = "username"  # use "username" as what defines users' username
    REQUIRED_FIELDS = ["email", "phone_number"]
'''


# abstracting user model from AbstractBaseUser (method 3)
class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin defines superusers, groups etc.
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Manager(BaseUserManager):  # when using AbstractBaseUser as default, a manager should be defined to create users
    def create_user(self, email, password):
        pass  # user creation process should be added here

    def create_superuser(self, email, password):
        pass  # superuser creation process should be added here
