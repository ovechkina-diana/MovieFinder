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


#IndexView для отображения главной страницы,
# наследуется от класса TemplateView  фреймворка Django
class IndexView(TemplateView):
    # шаблон HTML, который будет использоваться для отображения страницы
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        # объект контекста, который содержит данные, передаваемые в шаблон
        context = super().get_context_data(**kwargs)
        # если пользователь аутентифицирован, получаем профиль пользователя из модели UserProfile
        # на основе текущего пользователя request.user.
        # затем получаем жанры user_genres, связанные с пользователем,
        # и выбираем 10 фильмов films_on_genre, относящихся к этим жанрам.
        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)
            user_genres = user_profile.genres.all()
            films_on_genre = Film.objects.filter(genre__in=user_genres)[:10]
            # в контекст добавляем films_on_genre, films, genre
            context['films_on_genre'] = films_on_genre
        context['films'] = Film.objects.all()[:10]
        context['genres'] = Genre.objects.all()
        # получаеv значение из сессии, которое будет использовано для отображения или скрытия модального окна на странице
        context['show_genre_modal'] = self.request.session.pop('show_genre_modal', False)
        #  возвращаем обновленный контекст для использования в шаблоне
        return context

# определяется класс представления FilmDeatilView для отображения детальной информации фильма,
# наследуется от класса DetailView фреймворка Django
class FilmDeatilView(DetailView):
    # указывет на модель, с которой будет работать представление
    model = Film
    # шаблон HTML, который будет использоваться для отображения страницы
    template_name = 'main/movie-detail.html'
    # имя переменной, которая будет использоваться для доступа к объекту модели в шаблоне
    context_object_name = 'film'

    # обрабатывает POST-запрос, отправленный со страницы ддетальной информации фильма
    def post(self, request, slug):
        film = self.get_object()
        # получаем значение из POST-запроса, указывающее, был ли фильм просмотрен
        is_viewed = request.POST.get('is_viewed') == 'true'  # Преобразовать значение checkbox в тип bool

        # если фильм был когда-то отмечен, то изменяет занчение в бд, иначе создает новое
        enrollment, created = Enrollment.objects.get_or_create(user=request.user.userprofile, film=film)
        # помечаем фильм ка как прсомотренный и сохраняем изменения
        enrollment.isViewed = is_viewed
        enrollment.save()

        return JsonResponse({'status': 'success'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # получаем текущего пользователя
        user = self.request.user
        # Если пользователь аутентифицирован, то получаем объект фильма и
        # связанную с ним запись из таблицы Enrollment для данного пользователя
        if user.is_authenticated:
            film = self.get_object()
            enrollment = Enrollment.objects.filter(user__user=user, film=film).first()
            # добавляем переменную enrollment в контекст, содержащую информацию о просмотре фильма пользовател
            context['enrollment'] = enrollment
        return context

#  представление для обработки запроса списка фильмов на веб-странице
def movie_list(request):
    # получаем значения параметра "genres" и "years" из GET-запроса
    genres = request.GET.get('genres')
    years = request.GET.get('years')
    # получаем все объекты из таблицы Film
    films = Film.objects.all()

    # преобразуем полученную строку в список целочисленных значений и фильтруем фильмы,
    # оставляя только те, которые имеют указанные  жанры
    if genres:
        genre_list = [int(genre) for genre in genres.split(',')]
        films = films.filter(genre__in=genre_list)

    # преобразуем полученную строку в список целочисленных значений и фильтрует фильмы,
    # оставляя только те, которые имеют указанные  года
    if years:
        year_list = [int(year) for year in years.split(',')]
        films = films.filter(year__in=year_list)
    # удаляем повторяющиеся фильмы, так как в жанрах и годах могут быть одинковые
    films = films.distinct()
    # создаем словарь data с ключом 'films', содержащим отфильтрованные фильмы
    data = {
        'films': films
    }
    # возвращаем ответ с отображением шаблона и передачей словаря data в качестве контекста шаблона
    return render(request, 'main/movie-list.html', data)

# представление Django для отображения рекомендуемых фильмов
def movies_rec(request):
    # получаем все объекты из таблиц Genre и сортируем их по полю name в порядке возрастания
    genres = Genre.objects.all().order_by('name')
    # Получаем все объекты из таблицы Film
    films = Film.objects.all()
    # получаем список уникальных значений поля year из модели Film, сортирует их в порядке убывания
    years = Film.objects.values_list('year', flat=True).distinct().order_by('-year')
    # возвращаем ответ с отображением шаблона и передачей словаря,
    # содержащего genres, films и years, в качестве контекста шаблона
    return render(request, 'main/movies-rec.html', {'genres': genres, 'films': films, 'years': years})























