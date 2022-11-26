from django import forms

from movies.models import Movie, MovieComment


class MovieAddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'avatar', 'genres']


class CommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['title', 'text']
