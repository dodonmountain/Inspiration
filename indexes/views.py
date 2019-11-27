from django.shortcuts import render,get_object_or_404, redirect
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

def rater_review(request,user_id):
    rater_star_list = list(map(int, list(map(str, request.GET.get('v').split('/')))[1:]))
    rsl = []
    for i in range(30):
        if not i & 1:
            rsl.append((rater_star_list[i], rater_star_list[i+1]))
    for sc, mv in rsl:
        Review.objects.create(
            user = request.user,
            content = '',
            score = sc,
            movie = get_object_or_404(Movie,pk=mv)
        )
    return redirect('indexes:index')