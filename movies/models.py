from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=30)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies_user', blank=True)

class Review(models.Model):
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

'''
class Movie(models.Model):
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    video = models.BooleanField()
    poster_path = models.CharField(max_length=140)
    id = models.IntegerField(primary_key=True)
    adult = models.BooleanField()
    backdrop_path = models.CharField(max_length=140)
    original_language = models.CharField(max_length=10)
    original_title = models.CharField(max_length=100)
    genre_ids = ListCharField(
        base_field=models.CharField(max_length=10),
        size = 10,
        max_length = (11*10)
    )
    title = models.CharField(max_length=30)
    vote_average = models.FloatField()
    overview = models.TextField()
    release_date = DataField(input_formats=settings.DATE_INPUT_FORMATS)
'''