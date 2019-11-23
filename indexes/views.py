from django.shortcuts import render,get_object_or_404
from movies.models import Movie
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    movies = Movie.objects.all()
    movies = movies[:50]
    context = {
        'movies':movies
    }
    return render(request, 'index.html', context)

def welcome(request):
    return render(request, 'welcome.html')