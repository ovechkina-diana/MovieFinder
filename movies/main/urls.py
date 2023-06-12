
from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.IndexView.as_view(), name='home'),
    path('about', views.about, name='about'),
    path('movies', views.movies, name='movies'),
    path('movies-selection/<str:scrolling>/', views.MovieSelection.as_view(), name='movies-selection'),
    # path('movie-selection/', views.MovieSelection.as_view(), name='movie-selection'),
    # path('movie-detail', views.movie_detail, name='movie-detail'),
    #  path('<int:pk>', views.FilmDeatilView.as_view(), name='movie-detail'),
 # path('<str:title>', views.FilmDeatilView.as_view(), name='movie-detail'),
    path('film/<slug:slug>', views.FilmDeatilView.as_view(), name='movie-detail'),
    path('movies-rec', views.movies_rec, name='movies-rec'),
    # path('profile', views.profile, name='profile'),
    # path('register', views.register, name='register'),
    path('movies-rec/', views.movies_rec, name='movies-rec'),
    path('movie-list/', views.movie_list, name='movie-list')
]