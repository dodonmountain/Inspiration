from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User
from movies.models import Movie, Review

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
        A, B, C = 0,0,0
        if len(same_movies) > 1:
            for movie in same_movies:
                a = my_review.filter(movie=movie)[0].score *5
                b = other_review.filter(movie=movie)[0].score * 5
                A += a*a
                B += b*b
                C += a*b
            try:
                vs[other.id] = C / (A**(0.5) * B**(0.5))
                # print(vs[other.id])
            except:
                pass
    sorted_vs = sorted(vs.items(), key=lambda kv: kv[1],reverse=True)
    for v in sorted_vs[:20]:
        user = User.objects.get(pk=v[0])
    for a in sorted_vs[:20]:
        print(a)
        for same in my_movies & Movie.objects.filter(review__user_id=a):
            print(same.title)
    return sorted_vs[:20]

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
    

