from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Review,Genre , People, Credit, Trailer, MovieImage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
import numpy as np
from accounts.models import User

def translate(q): # 파파고 번역
    request_url = "https://openapi.naver.com/v1/papago/n2mt"
    headers= {"X-Naver-Client-Id": "fluVcHalFaa3gvtccvyu", "X-Naver-Client-Secret":"5y_p9Q86kf"}
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
                print(actor.people.name)
            except:
                print('movie',id)
                print('people',cast['id'])
## 영화 저장 , 장르 - 영화 MTM
def movie_save(id):
    if not Movie.objects.filter(pk=id):
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

# f115f7077bf79f6f7fd3227c5ba7f281
def movies_data(page_num): # popular,top_rated 중에서 페이지에 있는 영화 id값 확인
    # movies_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&page={page_num}&region=KR'
    movies_url = f'https://api.themoviedb.org/3/discover/movie?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&sort_by=popularity.desc&page={page_num}&vote_count.gte=10&with_original_language=ko'
    response = requests.get(movies_url).json().get('results')
    print('총 ' ,len(response) , '개')
    tmp = 0
    for r in response:
        id = r.get('id')
        movie_save(id)
        image_save(id)
        trailer_save(id)
        people_save(id)
        credit_save(id)
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

def trailer_save(id):
    if not Trailer.objects.filter(movie_id=id):
        trailers_url = f'https://api.themoviedb.org/3/movie/{id}/videos?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR'
        trailers = requests.get(trailers_url).json().get('results')
        for trailer in trailers:
            if trailer['site'] =='YouTube' and trailer['type'] == 'Trailer':
                Trailer.objects.create(
                    key = trailer['key'],
                    name = trailer['name'],
                    movie_id = id
                )

def image_save(id):
    if not MovieImage.objects.filter(movie_id=id):
        images_url = f'https://api.themoviedb.org/3/movie/{id}/images?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&include_image_language=ko'
        posters = requests.get(images_url).json().get('posters')
        try:
            for poster in posters:
                MovieImage.objects.create(
                    file_path = poster['file_path'],
                    movie_id = id
                )
        except:
            pass

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    # for i in range(15,18):
    #     movies_data(i)
    return render(request,'movies/index.html',{
        'movies':movies
    })

def detail(request,movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    all_review = Review.objects.filter(movie_id=movie_pk)
    if len(all_review):
        avg = sum(map(lambda x:x.score,all_review))/len(all_review)
    else:
        avg = 0
    reviews = Review.objects.filter(movie_id=movie_pk, user_id = request.user.pk)
    if reviews:
        review = reviews[0]
        context = {
            'review' : review,
        }
    else:
        movie = get_object_or_404(Movie,pk=movie_pk)
        context = {
            'review' : False
        }
    context['movie'] = movie
    context['avg'] = round(avg,2)
    context['credits'] = movie.credit_set.all().order_by('order')
    return render(request,'movies/detail.html',context)

@require_POST
def review(request,movie_pk):
    review = Review.objects.create(
        user = request.user,
        content = request.POST.get('content') or '',
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
    review.content = request.POST.get('content') or review.content or ''
    review.score = request.POST.get('score') or review.score
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
    # search_url = f'https://api.themoviedb.org/3/search/movie?api_key=f115f7077bf79f6f7fd3227c5ba7f281&language=ko-KR&query={query}&page=1&include_adult=false'
    # title_movies = requests.get(search_url).json().get('results')
    
    asdf_movies = Movie.objects.filter(overview__contains=query)
    overview_movies = asdf_movies.difference(title_movies)
    actors = People.objects.filter(name__contains=query)
    context = {
        "title_movies" : title_movies,
        "overview_movies" : asdf_movies,
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

def create(request,id):
    if not Movie.objects.filter(pk=id):
        print('없')
        movie_save(id)
    image_save(id)
    trailer_save(id)
    people_save(id)
    credit_save(id)
    return redirect('movies:detail',id)

def name_change(request,people_id):
    people = get_object_or_404(People, pk=people_id)
    people.name = request.GET.get('name')
    people.save()
    return redirect('movies:actor', people_id )

def genres(request):
    genres = Genre.objects.all()
    return render(request, 'movies/genres.html',{'genres':genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    count = User.objects.filter(username__contains=genre.name).count()

    count_movies = Movie.objects.filter(vote_count__gte=3000)
    ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    total = count_movies | ko_movies
    filter = total.filter(genres__id=genre_id)
    context = {
        'genre' : genre,
        'filter' : filter,
        'count' : count,
    }
    return render(request,'movies/genre_detail.html', context )

def make_fake(request,genre_id):
    genre = get_object_or_404(Genre,pk=genre_id)
    count_movies = Movie.objects.filter(vote_count__gte=3000)
    ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    total = count_movies | ko_movies
    filter = total.filter(genres__id=genre_id)
    other = count_movies.difference(filter)
    others = other.exclude(genres__id=genre_id)
    count = User.objects.filter(username__contains=genre.name).count()
    u = User.objects.create(email=f'{genre.name}{count+1}@inspiration.com',
        username=f'{genre.name}{count+1}',
        first_name = f'{genre.name}{count+1}',
        password='password'
    )
    for movie in np.random.choice(filter,min(40,len(filter)//2),replace =False):
            s = np.random.normal(movie.vote_average+0.7, 2)
            if s > 10:
                s = 10
            elif s < 0:
                s = 0 - s
            Review.objects.create(
                score = round(s+0.5),
                content = '',
                movie_id = movie.pk,
                user_id = u.id
            )
    for movie in np.random.choice(other,min(30,len(other)//2),replace =False):
        s = np.random.normal(movie.vote_average-1, 2)
        if s > 10:
            s = 10
        elif s < 1:
            s = 2 - s
        Review.objects.create(
            score = round(s-0.3),
            content = '',
            movie_id = movie.pk,
            user_id = u.id
        )
    return redirect('movies:genre_detail',genre_id)


