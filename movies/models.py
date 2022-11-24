from django.db import models
from django.db.models import Avg

from comments.models import AbstractComment
from config import settings
from django.core.validators import MaxValueValidator, MinValueValidator  # imported so can be used in rating validation


# from users.models import User


class Genre(models.Model):
    title = models.CharField(max_length=63)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    # auto_now_add: the time the instance was created
    # auto_now: the time the instance was modified

    def __str__(self):
        return self.title
    # lets us see the results by movie TITLE


class Role(models.Model):
    title = models.CharField(max_length=63)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Crew(models.Model):
    MALE = 1
    FEMALE = 2
    GENRE_CHOICE = ((MALE, 'Male'), (FEMALE, 'Female'))
    # a tuple is used here because the dataset should be iterable
    # lists can also be used

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENRE_CHOICE, default=MALE)
    avatar = models.ImageField(upload_to='crew/avatars', null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='movies/avatars', null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    crew = models.ManyToManyField(Crew, through='MovieCrew')
    # Django automatically creates a pivot table for any ManyToMany relation
    # We use 'through' attribute to customize our pivot table
    is_valid = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def get_description(self):
        # creating a function in order to lower the description while returning it
        return self.description.lower()

    def __str__(self):
        return self.title

    # show the object by its title

    # def clean(self):
    #     raise ValidationError('Not good')

    # below property and function is used to calculate and display average rating for each movie
    @property
    def average_rating(self):
        rate = self.ratings.all().aggregate(avg=Avg('rate'))
        return rate.get('avg') or 1  # used "or 1" so if no rate was set, it won't output None


class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'crew', 'role')
        # used to make two or more model fields to be true and unique
        # Meta classes are used to add or change a behavior in a class

    # below function is used to capitalize first letter of each movie's name
    def save(self, *args, **kwargs):
        self.movie = self.movie.caplitalize()


# the below class is used for commenting on movies
class MovieComment(AbstractComment):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


# the below class is used for commenting on crew members
class CrewComment(AbstractComment):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)


# BELOW MODEL IS CREATED FOR RATING ON MOVIES
class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_rating')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        # "movie" and "user" fields should be unified, because each user
        # should only be able to rate each movie at most 1 time

        # unique_together = ('user', 'movie') # this unifying method is deprecated

        # other method is using constraints
        constraints = [models.UniqueConstraint(fields=('user', 'movie'), name='unique_user_movie')]
