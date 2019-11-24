from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Review,Genre , People, Credit
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.core import serializers
import pprint

def translate(q): # 파파고 번역
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers= {"X-Naver-Client-Id": "1mql_fSo30DYAieQyV_o", "X-Naver-Client-Secret":"sXv8IqV5eH"}
    params = {"source": "en", "target": "ko", "text": q}
    response = requests.post(request_url, headers=headers, data=params)
    result = response.json()
    try:
        return result['message']['result']['translatedText']
    except:
        print(q)
        return q

## 영화 id값을 받아서 order 10까지 people 데이터 저장, 영화 - people MTM
def people_save(id):
    credits_url = f'https://api.themoviedb.org/3/movie/{id}/credits?api_key=f115f7077bf79f6f7fd3227c5ba7f281'
    credit = requests.get(credits_url).json()
    casts = credit['cast']
    crews = credit['crew']
    for cast in casts:
        if cast['order'] < 10:
            actor, created = People.objects.get_or_create(
                id = cast['id'],
                defaults={'name' : translate(cast['name']),
                'job' : 'Actor',
                'profile_path' : cast['profile_path']}
            )
            movie = Movie.objects.get(pk=id)
            movie.people.add(actor)
    for crew in crews:
        if crew['job'] == 'Director':
            director, created = People.objects.get_or_create(
                id = crew['id'],
                defaults={'name' : translate(crew['name']),
                'job' : 'Director',
                'profile_path' : crew['profile_path']}
            )
            movie = Movie.objects.get(pk=id)
            movie.people.add(director)

def credit_save(id):
    credits_url = f'https://api.themoviedb.org/3/movie/{id}/credits?api_key=f115f7077bf79f6f7fd3227c5ba7f281'
    credit = requests.get(credits_url).json()
    casts = credit['cast']
    crews = credit['crew']
    for cast in casts:
        if cast['order'] < 10:
            try:
                actor, created = Credit.objects.get_or_create(
                    credit_id = cast['credit_id'],
                    character = cast['character'],
                    order = cast['order'],
                    movie = Movie.objects.get(pk=id),
                    people = People.objects.get(id=cast['id'])
                )
                print(actor.movie, actor.people)
            except:
                print('movie',id)
                print('people',cast['id'])
## 영화 저장 , 장르 - 영화 MTM
def movie_save(id):
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
    print(movie.title, '등록완료')

def movies_data(page_num): # popular,top_rated 중에서 페이지에 있는 영화 id값 확인
    movies_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page={page_num}&region=KR'
    response = requests.get(movies_url).json().get('results')
    print('총 ' ,len(response) , '개')
    tmp = 0
    for r in response:
        id = r.get('id')
        if not Credit.objects.filter(movie_id=id):
            credit_save(id)
        # movies = Movie.objects.filter(pk=id)
        # if not movies:
        #     tmp += 1
        #     movie_save(id)
        #     credit_save(id)
        #     # people_save(id)
        # else:
        #     print(movies[0].title)        
    print('등록 ',tmp , '개')

def name_change(en):
    try:
        people = People.objects.filter(name=en.strip())[0]
        ko = translate(en)
        people.name = ko
        people.save()
        print(people.name)
    except:
        print(en)
        pass

# Create your views here.
def index(request):
    movies = Movie.objects.all()

    return render(request,'movies/index.html',{
        'movies':movies
    })


def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    reviews = Review.objects.filter(movie_id=movie_pk, user_id = request.user.pk)
    if reviews:
        review = reviews[0]
        context = {
            'review' : review
        }
    else:
        movie = get_object_or_404(Movie,pk=movie_pk)
        context = {
            'review' : False
        }
    context['movie'] = movie
    context['credits'] = movie.credit_set.all().order_by('order')
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
    actors = People.objects.filter(name__contains=query)
    context = {
        "title_movies" : title_movies,
        "overview_movies" : overview_movies,
        'actors' : actors,
        'query' : query,
    }
    return render(request,'movies/search.html',context)

def actor(request,id):
    people = get_object_or_404(People,pk=id)
    print(people)
    context = {
        'people' : people
    }
    return render(request,'movies/actor.html',context)