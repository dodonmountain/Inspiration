from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    video = models.BooleanField()
    poster_path = models.CharField(max_length=140)
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
    release_date = models.DateField()

class Review(models.Model):
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
