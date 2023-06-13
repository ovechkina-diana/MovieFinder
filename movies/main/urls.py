
from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('movies-selection/<str:scrolling>/', views.MovieSelection.as_view(), name='movies-selection'),
    path('film/<slug:slug>', views.FilmDeatilView.as_view(), name='movie-detail'),
    path('movies-rec', views.movies_rec, name='movies-rec'),
    path('movies-rec/', views.movies_rec, name='movies-rec'),
    path('movie-list/', views.movie_list, name='movie-list')
]