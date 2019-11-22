from django.shortcuts import render,get_object_or_404
from movies.models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    movies = movies[:50]
    context = {
        'movies':movies
    }
    return render(request, 'index.html', context)