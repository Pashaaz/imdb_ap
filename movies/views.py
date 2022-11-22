from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from movies.forms import MovieAddForm
from movies.models import Movie


def movies_list(request):
    movies = Movie.objects.all()
    user = User
    context = {
        'movies': movies,
        'User': user
    }
    return render(request, 'movies/movies_list.html', context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)
    genre = movie.genres.all()
    crew = movie.crew.all()
    user = User

    context = {
        'movie': movie,
        'genre': genre,
        'crew': crew,
        'User': user
    }

    return render(request, 'movies/movie_detail.html', context=context)


def movie_add(request, form=None):
    user = User
    if request.method == 'GET':
        if not form:
            form = MovieAddForm()

        return render(request, 'movies/movie_add.html', context={'form': form, 'User': user})

    elif request.method == 'POST':
        form = MovieAddForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('movies_list')

    form = MovieAddForm(request.POST, request.FILES)
    request.method = 'GET'
    # return movie_add(request, form)
    return render(request, 'movies/movie_add.html', context={'form': form})
