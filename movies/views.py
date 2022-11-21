from django.contrib.auth.models import User
from django.shortcuts import render

from movies.models import Movie


def movies_list(request):
    movies = Movie.objects.all()
    if User.is_authenticated:
        user = True
    else:
        user = False
    context = {
        'movies': movies,
        'User': user
    }
    return render(request, 'movies/movies_list.html', context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)
    genre = movie.genres.all()
    crew = movie.crew.all()
    user = User.is_authenticated

    context = {
        'movie': movie,
        'genre': genre,
        'crew': crew,
        'User': user
    }

    return render(request, 'movies/movie_detail.html', context=context)


def movie_add(request):
    pass
