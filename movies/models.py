from django.db import models
from django.core.exceptions import ValidationError


class Genre(models.Model):
    title = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    # auto_now_add: the time the instance was created
    # auto_now: the time the instance was modified

    def __str__(self):
        return self.title
    # the magic method that lets us see the results by movie TITLE


class Role(models.Model):
    title = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Crew(models.Model):
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )
    # we used a tuple here because the dataset should be iterable (can also use lists)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=MALE)
    avatar = models.ImageField(upload_to='crew/avatars/', null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='movies/avatars/', null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    crew = models.ManyToManyField(Crew, through='MovieCrew')
    is_valid = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    # def get_description(self):
    #    return self.description.lower()

    def __str__(self):
        return self.title

    # show the object by its title


class MovieCrew(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'crew', 'role')

    # Django unique_together is used to make two or more model fields to be unique

    # https://www.geeksforgeeks.org/meta-class-in-models-django/

    # Meta classes are used to add or change a behavior in your class
