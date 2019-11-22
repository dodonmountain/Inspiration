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
import pprint

def genres_data():
    genres_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
    response = requests.get(genres_url).json().get('genres')
    for r in response:
        genre = Genre(**r)
        genre.save()

def movies_data(page_num):
    movies_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page={page_num}&region=KR'
    response = requests.get(movies_url).json().get('results')
    print('총 ' ,len(response) , '개')
    tmp = 0
    for r in response:
        id = r.get('id')
        if not Movie.objects.filter(pk=id):
            tmp += 1
            detail_url = f'https://api.themoviedb.org/3/movie/{id}?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
            detail = requests.get(detail_url).json()
            
            movie = Movie.objects.create(
                adult = detail.get('adult'),
                backdrop_path = detail.get('backdrop_path'),
                budget = detail.get('budget'),
                id = detail.get('id'),
                original_language = detail.get('original_language'),
                overview = detail.get('overview'),
                popularity = detail.get('popularity'),
                poster_path = detail.get('poster_path'),
                release_date = detail.get('release_date'),
                revenue = detail.get('revenue'),
                runtime = detail.get('runtime'),
                status = detail.get('status'),
                tagline = detail.get('tagline'),
                title = detail.get('title'),
                video = detail.get('video'),
                vote_average = detail.get('vote_average'),
                vote_count = detail.get('vote_count')
            )
            for r in detail.get('genres'):
                genre = Genre.objects.get(pk=r.get('id'))
                movie.genres.add(genre)
            movie.save()
    print('등록 ',tmp , '개')

# Create your views here.
def index(request):
    movies = Movie.objects.all()
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
    reviews = Review.objects.filter(movie_id=movie_pk, user_id = request.user.pk)
    if reviews:
        review = reviews[0]
        context = {
            'movie':movie,
            'review' : review
        }
    else:
        movie = get_object_or_404(Movie,pk=movie_pk)
        context = {
            'movie':movie,
            'review' : False
        }
    return render(request,'movies/detail.html',context)

@require_POST
def review(request,movie_pk):
    review = Review.objects.create(
        user = request.user,
        content = request.POST.get('content'),
        score = request.POST.get('score'),
        movie = get_object_or_404(Movie,pk=movie_pk)
    )
    return redirect('movies:detail',movie_pk)

def review_delete(request,movie_pk, review_pk):
    review = get_object_or_404(Review,pk=review_pk)
    review.delete()
    return redirect('movies:detail',movie_pk)

def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    review.content = request.POST.get('content')
    review.score = request.POST.get('score')
    review.save()
    return redirect('movies:detail',movie_pk)

@login_required
@require_POST
def like(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    if request.user in movie.like_user.all():
        movie.like_user.remove(request.user)
    else:
        movie.like_user.add(request.user)
    return redirect('movies:detail',movie_pk)

def search(request):
    query = request.GET.get('q')
    title_movies = Movie.objects.filter(title__contains=query)

    asdf_movies = Movie.objects.filter(overview__contains=query)
    overview_movies = asdf_movies.difference(title_movies)
    context = {
        "title_movies" : title_movies,
        "overview_movies" : overview_movies
    }
    return render(request,'movies/search.html',context)