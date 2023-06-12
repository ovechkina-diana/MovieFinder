from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views import View

from .models import UserProfile

from .forms import RegisterUserForm, LoginUserForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('main:profile')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        UserProfile.objects.create(user=user)

        self.request.session['show_genre_modal'] = True
        return redirect('main:home')

    def get_success_url(self):
        return reverse_lazy('main:home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Вход"
        return context

    def get_success_url(self):
        return reverse_lazy('main:home')

def genre_selection(request):
    if request.user.is_authenticated and request.method == 'GET':
        genres = request.GET.get('genres')
        genre_list = [int(genre) for genre in genres.split(',')]
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.genres.clear()  # Очищаем список жанров пользователя
        user_profile.genres.add(*genre_list)  # Добавляем выбранные жанры

        return HttpResponse('Success')
    else:
        return HttpResponse('Method Not Allowed', status=405)


def logout_user(request):
    logout(request)
    return redirect('user:login')

def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_genres = user_profile.genres.all()
    user_viewed_films = user_profile.films.filter(enrollment__isViewed=True)

    return render(request, 'user/profile.html', {'genres': user_genres, 'films': user_viewed_films})


