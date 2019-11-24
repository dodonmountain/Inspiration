from django.contrib import admin
from django.urls import path,include
from accounts import urls



urlpatterns = [
    path('', include('indexes.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('movies/',include('movies.urls')),
    path('accounts/', include('allauth.urls')),
]
