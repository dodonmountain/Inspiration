from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField

# Create your models here.
class Genre(models.Model):  
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class Movie(models.Model):
    adult = models.BooleanField(null=True)
    backdrop_path = models.CharField(max_length=140,null=True)
    budget = models.IntegerField()
    genres = models.ManyToManyField(Genre,related_name='genre_movies',blank=True)
    id = models.IntegerField(primary_key=True)
    original_language = models.CharField(max_length=10)
    overview = models.TextField(null=True)
    popularity = models.FloatField()
    poster_path = models.CharField(max_length=140,null=True)
    release_date = models.DateField()
    revenue = models.IntegerField()
    runtime = models.IntegerField(null=True)
    status = models.CharField(max_length=40)
    tagline = models.TextField(null=True)
    title = models.CharField(max_length=30)
    video = models.BooleanField()
    vote_average = models.FloatField()
    vote_count = models.IntegerField()

class Review(models.Model):
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
