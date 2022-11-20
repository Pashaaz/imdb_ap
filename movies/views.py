from django.shortcuts import render

from movies.models import Movie


def movies_list(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/movies_list.html', context=context)
