from django.urls import path
from . import views


app_name = 'indexes'

urlpatterns = [
    path('index/',views.index,name="index"),
    path('',views.welcome, name="welcome"),
    path('rater/', views.rater, name="rater"),
    path('index/<int:genre_id>/',views.genre_select,name="genre_select"),
    path('rater/rater_review/<int:user_id>', views.rater_review, name="rater_review")
]