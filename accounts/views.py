from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User
from movies.models import Movie, Review
import numpy as np

# def my_page(request):
def signup(request):
    if request.user.is_authenticated:
        return redirect('indexes:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('indexes:index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('indexes:index')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
        }
    return render(request, 'accounts/form.html', context)

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            update_session_auth_hash(request, form.save())
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def user_like_genre(user):
    user_genres = {}
    for review in user.review_set.all(): # 유저의 리뷰들을 다 가져와서
        if review.score:
            for genre in review.movie.genres.all():
                if genre.name not in user_genres:
                    user_genres[genre.name] = [0,0]
                user_genres[genre.name][0] += review.score
                user_genres[genre.name][1] += 1
    for idx,value in user_genres.items():
        user_genres[idx] = value[0]/value[1]
    return user_genres

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
    for i in sorted_vs[2:15]:
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
        tmp =[] # 쿼리, 예상평점, 정확도
        tmp.append(Movie.objects.filter(pk=sorted_movie[i][0]))
        tmp.append(round(sorted_movie[i][1][1]/sorted_movie[i][1][0],2))
        tmp.append(round(sorted_movie[i][1][2]/sorted_movie[i][1][0] * 100,1))
        if tmp[1] > 6 and tmp[2] > 10 :
            arr.append(tmp)
    return arr

@login_required
def userDetail(request, user_id):
    # if user_id == request.user.id:
    user = get_object_or_404(User, pk=user_id)
    my_review = user.review_set.filter()
    my_movies = Movie.objects.filter(review__user=user)
    one_movies = Movie.objects.filter(review__user_id=1)
    same_movie = my_movies & one_movies
    context = {
        'userinfo' : user,
        'user_like_genre' : user_like_genre(user),
        'my_review' : my_review,
        # 'vs' : vs_user(user)
    }
    return render(request, 'accounts/detail.html', context)
    # return redirect('accounts:login')

def select(request, user_id):
    # movies = Movie.objects.filter(vote_count__lt=3000).filter(popularity__gte=50)
    count_movies = Movie.objects.filter(vote_count__gte=3000)
    ko_movies = Movie.objects.filter(original_language='ko').filter(popularity__gte=5)
    total = count_movies | ko_movies
    total = np.random.choice(total,100,replace=False)
    context = {'total':total}
    return render(request,'accounts/select.html',context)