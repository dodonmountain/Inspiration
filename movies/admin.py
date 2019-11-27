from django.contrib import admin
from .models import Movie, People, Credit, MovieImage, Review
# Register your models here.
admin.site.register(Movie)
admin.site.register(People)
admin.site.register(Credit)
admin.site.register(MovieImage)
admin.site.register(Review)