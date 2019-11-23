from django.contrib import admin
from .models import Movie, People, Credit
# Register your models here.
admin.site.register(Movie)
admin.site.register(People)
admin.site.register(Credit)