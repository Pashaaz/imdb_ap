from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from movies.forms import MovieAddForm
from movies.models import Movie, MovieCrew


def movies_list(request):
    movies = Movie.objects.all()
    user = User
    context = {
        'movies': movies,
        'User': user
    }
    return render(request, 'movies/movies_list.html', context=context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = movie.genres
    movie_crew = MovieCrew.objects.filter(movie=movie).select_related('crew', 'role')
    directors = []
    writers = []
    actors = []
    for crew in movie_crew:
        if crew.role.title == 'Director':
            directors.append(str(crew.crew.first_name)+str(crew.crew.last_name))
        elif crew.role.title == 'Writer':
            writers.append(str(crew.crew.first_name)+str(crew.crew.last_name))
        elif crew.role.title == 'Actor':
            actors.append(str(crew.crew.first_name)+str(crew.crew.last_name))

    context = {'movie': movie,
               'Directors': directors,
               'Writers': writers,
               'Actors': actors,
               'Genres': genres}

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
