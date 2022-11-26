from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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


# class Manager(BaseUserManager):  # when using AbstractBaseUser as default, a manager should be defined to create users
#     def create_user(self, email, password):
#         pass  # user creation process should be added here
#
#     def create_superuser(self, email, password):
#         pass  # superuser creation process should be added here


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        # Create and save user
        if not email:
            raise ValueError(_('Email Required!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser staff must be True'))
        if extra_fields.get(_('is_superuser')) is not True:
            raise ValueError(_('Superuser superuser must be True'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):  # PermissionsMixin defines superusers, groups etc.
    first_name = models.CharField(max_length=150, blank=True, verbose_name="first name")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="last name")
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
