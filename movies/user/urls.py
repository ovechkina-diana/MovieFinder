
from django.urls import path
from . import views


urlpatterns = [
    # path('profile', views.profile, name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    # path('genre-selection/', views.GenreSelectionView.as_view(), name='genre_selection'),
    path('genre-selection/', views.genre_selection, name='genre_selection'),
    # path('register/', views.CombinedView.as_view(), name='register'),

]