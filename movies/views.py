from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from movies.forms import MovieAddForm, CommentForm
from movies.models import Movie, MovieCrew


def movies_list(request):
    movies = Movie.objects.all().filter(is_valid=True)

    context = {
        'movies': movies,
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
            directors.append(crew.crew.full_name())
        elif crew.role.title == 'Writer':
            writers.append(crew.crew.full_name())
        elif crew.role.title == 'Actor':
            actors.append(crew.crew.full_name())

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


def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'GET':
        form = MovieAddForm(instance=movie)
        context = {
            'form': form,
            'movie': movie
        }
        return render(request, 'movies/edit_movie_form.html', context=context)
    elif request.method == 'POST':
        form = MovieAddForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            context = {
                'form': form,
                'movie': movie
            }
            return redirect('movie_detail', pk=pk)
        else:
            form = MovieAddForm(instance=movie)
            context = {
                'form': form,
                'movie': movie
            }
            return render(request, 'movies/edit_movie_form.html', context=context)


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.is_valid = False
    movie.save()

    return redirect('movies_list')


def movie_comment(request, pk=None, comment_form=None):
    if request.method == 'GET':
        if not comment_form:
            comment_form = CommentForm()

        context_get = {
            'pk': pk,
            'form': comment_form
        }

        return render(request, 'movies/comment.html', context=context_get)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if comment_form.is_valid():
                comment_form.save(commit=False)
                comment_form.user = request.user
                comment_form.movie = pk
                comment_form.save()
            else:
                redirect('movie_comment', comment_form)

        else:
            return redirect('movie_comment', comment_form)

    return redirect('movie_detail')
