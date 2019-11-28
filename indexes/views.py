from django.shortcuts import render,get_object_or_404, redirect
from movies.models import Movie,Review, Genre
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.contrib.auth.decorators import login_required
import numpy as np
from accounts.models import User
from django.db.models import Avg, Count

# Create your views here.
@login_required
def index(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all().annotate(
        count = Count('review'),
        avg = Avg('review__score')
    ).filter(count__gte=30).order_by('-avg')[:30]
    context = {
        'genres' : genres,
        'movies' : movies
    }
    # count_movies = Movie.objects.filter(vote_count__gte=3000)
    # ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    # total = count_movies | ko_movies
    # my_review_movie = Movie.objects.filter(review__user=request.user)
    # total = total.difference(my_review_movie)
    # total = np.random.choice(total,50,replace =False)
    return render(request,'index.html',context)

def myindex(request):
    genres = Genre.objects.all()
    context = {
        'genres' : genres,
        'movies' : vs_user(request.user)
    }
    return render(request, 'myindex.html', context)


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

def vs_user(user):
    users = User.objects.all()
    my_movies = Movie.objects.filter(review__user=user)
    my_review = Review.objects.filter(user=user)
    vs={}
    for other in users:
        other_movies = Movie.objects.filter(review__user=other)
        other_review = Review.objects.filter(user=other)
        same_movies = my_movies & other_movies
        X,Y, XX,YY,XY,cnt = 0,0,0,0,0,0
        if len(same_movies) > 2:
            for movie in same_movies:
                a = my_review.filter(movie=movie)[0].score
                b = other_review.filter(movie=movie)[0].score
                X += a
                Y += b
                XX += a*a
                YY += b*b
                XY += a*b
                cnt += 1
            try:
                vs[other.id] = (XY-(X*Y)/cnt)/ (((XX-(X*X)/cnt) * (YY-(Y*Y)/cnt)) ** 0.5)
            except:
                pass
    sorted_vs = sorted(vs.items(), key=lambda kv: kv[1],reverse=True)
    movies = {}
    for i in sorted_vs[1:15]:
        for review in Review.objects.filter(user_id=i[0]):
            if review.movie_id in movies and review.score > 6:
                if not Review.objects.filter(user=user).filter(movie_id=review.movie_id):
                    movies[review.movie_id][0] += 1
                    movies[review.movie_id][1] += review.score
                    movies[review.movie_id][2] += i[1]
            else:
                movies[review.movie_id] = [1,review.score,i[1]]
    sorted_movie = sorted(movies.items(),key=lambda x: x[1] ,reverse=True)[:60]
    arr = []
    for i in range(len(sorted_movie)):
        if sorted_movie[i][1][0] > 1:
            tmp =[] # 쿼리, 예상평점, 정확도
            tmp.append(Movie.objects.filter(pk=sorted_movie[i][0])[0])
            tmp.append(round(sorted_movie[i][1][1]/sorted_movie[i][1][0],2))
            tmp.append(round(sorted_movie[i][1][2]/sorted_movie[i][1][0] * 100,1))
            if tmp[1] > 6 and tmp[2] > 30 :
                arr.append(tmp)
            # arr = sorted(arr, key=lambda x: x[1] * x[2],reverse=True)
    return arr

@login_required
def rater(request):
    count_movies = Movie.objects.filter(vote_count__gte=3000)
    ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    total = count_movies | ko_movies
    watched_movie = total.filter(review__user=request.user)
    movies = total.difference(watched_movie)
    movies = np.random.choice(movies,100,replace=False)
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