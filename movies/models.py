from django.db import models
from django.conf import settings
from django.conf import settings

# Create your models here.
class Genre(models.Model):  
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class People(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    job = models.CharField(max_length=10)
    profile_path = models.CharField(max_length=140,null=True)

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
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies',blank=True)
    people = models.ManyToManyField(People,blank=True)


class Review(models.Model):
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Credit(models.Model):
    credit_id = models.CharField(max_length=30,primary_key=True)
    character = models.CharField(max_length=50)
    order = models.IntegerField()
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    people = models.ForeignKey(People,on_delete=models.CASCADE)

class Trailer(models.Model):
    key = models.CharField(max_length=50,primary_key=True)
    name = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)

class MovieImage(models.Model):
    file_path = models.CharField(max_length=140,primary_key=True)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)