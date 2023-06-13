
from django.urls import path
from . import views

# определение маршрутов URL для приложение main

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    # в адресной строке, благодаря слагу отображаются названия конкретных фильмов, в зависимости от страницы
    path('film/<slug:slug>', views.FilmDeatilView.as_view(), name='movie-detail'),
    path('movies-rec', views.movies_rec, name='movies-rec'),
    path('movie-list/', views.movie_list, name='movie-list')
]