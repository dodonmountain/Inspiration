from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from IPython import embed
from tmdbv3api import TMDb
from tmdbv3api import Movie as film
from .models import Movie,Genre
from django.core import serializers

def genres_data():
    genres_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
    response = requests.get(genres_url).json().get('genres')
    for r in response:
        genre = Genre(**r)
        genre.save()
def movies_data(page_num):
    movies_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page={page_num}&region=KR'
    response = requests.get(movies_url).json().get('results')
    for r in response:
        id = r.get('id')
        detail_url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
        response = requests.get(movies_url).json()
        movie = Movie.objects.create(
            adult = response.get('adult'),
            backdrop_path = response.get('backdrop_path'),
            budget = response.get('budget'),
            genres = response.get('genres'),
            id = response.get('id'),
            original_language = response.get('original_language'),
            overview = response.get('overview'),
            popularity = response.get('popularity'),
            poster_path = response.get('poster_path'),
            release_date = response.get('release_date'),
            revenue = response.get('revenue'),
            runtime = response.get('runtime'),
            status = response.get('status'),
            tagline = response.get('tagline'),
            title = response.get('title'),
            video = response.get('video'),
            vote_average = response.get('vote_average'),
            vote_count = response.get('vote_count'),
        )


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    # genres_data()
    movies_data(1)
        # url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&page=1&language=ko-KR'
        # response = requests.get(url).json()
        # movies = response.get('results')
        # url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page=3&region=KR'
        # response = requests.get(url).json().get('results')
        # print(requests.get(url))
        # for r in response:
        #     movie = Movie(**r)
        #     movie.save()
        # serialized_queryset = serializers.serialize('json', [results])
        # print(serialized_queryset)
        # tmdb = TMDb()
        # tmdb.api_key = 'f115f7077bf79f6f7fd3227c5ba7f281'
        # tmdb.language = 'ko'
        # movies = film()
        # movie = movies.search('겨울왕국')
        # recommendations = movies.recommendations(movie_id=496243)
        # embed()
    return render(request,'movies/index.html',{
        'movies':movies
    })


def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    form = ReviewForm()
    context = {
        'movie':movie,
        'form':form
    }
    return render(request,'movies/detail.html',context)

@require_POST
def review(request,movie_pk):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.movie = get_object_or_404(Movie,pk=movie_pk)
        review.user = request.user
        review.save()
        return redirect('movies:detail',movie_pk)

def review_delete(request,movie_pk, review_pk):
    review = get_object_or_404(Review,pk=review_pk)
    review.delete()
    return redirect('movies:detail',movie_pk)

def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = get_object_or_404(Movie,pk=movie_pk)
            review.user = request.user
            review.save()
            return redirect('movies:detail',movie_pk)
    form = ReviewForm(instance=review)
    return render(request, 'accounts/form.html', {'form':form})

@login_required
@require_POST
def like(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.user in movie.like_user.all():
        movie.like_user.remove(request.user)
    else:
        movie.like_user.add(request.user)
    return redirect('movies:detail',movie_pk)
