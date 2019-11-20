from django.urls import path
from . import views


app_name = 'indexes'

urlpatterns = [
    path('',views.index,name="index")
]