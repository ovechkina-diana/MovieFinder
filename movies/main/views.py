from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from .models import Actor, Genre, Director, Film, Country
from django.views.generic import DetailView, TemplateView, ListView
from slugify import slugify
from django.views import View
from django.http import JsonResponse

from user.models import UserProfile, Enrollment



class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
      
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            user_genres = user_profile.genres.all()
            films_on_genre = Film.objects.filter(genre__in=user_genres)[:10]
            context['films_on_genre'] = films_on_genre
        context['films'] = Film.objects.all()[:10]
        context['genres'] = Genre.objects.all()
        context['show_genre_modal'] = self.request.session.pop('show_genre_modal', False)
        return context


class FilmDeatilView(DetailView):
    model = Film
    template_name = 'main/movie-detail.html'
    context_object_name = 'film'

    def post(self, request, slug):
        film = self.get_object()
        is_viewed = request.POST.get('is_viewed') == 'true'  

        enrollment, created = Enrollment.objects.get_or_create(user=request.user.userprofile, film=film)
        enrollment.isViewed = is_viewed
        enrollment.save()

        return JsonResponse({'status': 'success'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            film = self.get_object()
            enrollment = Enrollment.objects.filter(user__user=user, film=film).first()
            context['enrollment'] = enrollment
        return context

def movie_list(request):
    genres = request.GET.get('genres')
    years = request.GET.get('years')
    films = Film.objects.all()

    if genres:
        genre_list = [int(genre) for genre in genres.split(',')]
        films = films.filter(genre__in=genre_list)

    if years:
        year_list = [int(year) for year in years.split(',')]
        films = films.filter(year__in=year_list)
    films = films.distinct()
    data = {
        'films': films
    }
    return render(request, 'main/movie-list.html', data)

def movies_rec(request):
    genres = Genre.objects.all().order_by('name')
    films = Film.objects.all()
    years = Film.objects.values_list('year', flat=True).distinct().order_by('-year')
    return render(request, 'main/movies-rec.html', {'genres': genres, 'films': films, 'years': years})























