from django.shortcuts import render

from movies.models import Movie


def movies_list(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'movies/movies_list.html', context=context)


def movie_detail(request, pk):
    movie = Movie.objects.get(id=pk)
    genre = movie.genres.all()
    crew = movie.crew.all()

    context = {
        'movie': movie,
        'genre': genre,
        'crew': crew
    }

    return render(request, 'movies/movie_detail.html', context=context)
