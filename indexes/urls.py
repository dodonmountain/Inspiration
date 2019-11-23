from django.urls import path
from . import views


app_name = 'indexes'

urlpatterns = [
    path('index/',views.index,name="index"),
    path('',views.welcome, name="welcome")
]