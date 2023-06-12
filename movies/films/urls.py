
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.films_home, name='films-home'),
    re_path(r'^create', views.create, name='create'),
    path('<int:pk>', views.FilmsDeatilView.as_view(), name='film-detail'),
    path('<int:pk>/update', views.FilmsUpdateView.as_view(), name='film-update'),
    path('<int:pk>/delete', views.FilmsDeleteView.as_view(), name='film-delete'),

]