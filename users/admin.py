from django.contrib import admin

from users.models import User


# Register your models here.
# Created classes should also be added here, based on models

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)


admin.site.register(User, UserAdmin)
