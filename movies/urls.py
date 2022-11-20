from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from movies.views import movies_list, movie_detail

urlpatterns = [
    path('', movies_list, name='movies_list'),
    path('movies/<int:pk>', movie_detail, name='movie_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
