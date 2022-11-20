from django.contrib import admin
from movies.models import *

admin.site.register(Genre)
admin.site.register(Role)
admin.site.register(Crew)
admin.site.register(Movie)
admin.site.register(MovieCrew)
