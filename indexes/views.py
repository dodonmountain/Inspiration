from django.shortcuts import render,get_object_or_404
from movies.models import Movie,Review, Genre
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.contrib.auth.decorators import login_required
import numpy as np

# Create your views here.
@login_required
def index(request):
    genres = Genre.objects.all()
    count_movies = Movie.objects.filter(vote_count__gte=3000)
    ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    total = count_movies | ko_movies
    my_review_movie = Movie.objects.filter(review__user=request.user)
    total = total.difference(my_review_movie)
    total = np.random.choice(total,50,replace =False)
    context = {
        'movies': total,
        'genres' : genres
    }
    return render(request, 'index.html', context)

def genre_select(request,genre_id):
    if genre_id == 1:
        movies = Movie.objects.filter(original_language='ko').order_by('-vote_count')
    else:
        movies = Movie.objects.filter(genres__id=genre_id).order_by('-vote_count')
    context = {
        'movies':movies
    }
    return render(request,'genre_select.html',context)

def welcome(request):
    return render(request, 'welcome.html')

@login_required
def rater(request):
    movies = Movie.objects.all()
    movies = movies[500:600]
    context = {
        'movies': movies
    }
    return render(request, 'rater.html', context)