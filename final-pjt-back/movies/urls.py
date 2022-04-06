from django.urls import path
from . import views

# app_name = 'movies'
urlpatterns = [
    path('random/', views.movie_random_list),
    path('playing/', views.movie_playing_list),
    path('genres/', views.movie_genre_list),
    path('all/', views.movie_all_list),
    path('<int:movie_id>/', views.movie_detail),
    path('recommend/', views.movie_recommend),
    path('add/', views.add_tmdb_data),
    
]