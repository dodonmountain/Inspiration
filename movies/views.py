from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(request):
    movies = Movie.objects.all()
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
