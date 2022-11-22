from django import forms

from movies.models import Movie


class MovieAddForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'release_date', 'avatar', 'genres']
