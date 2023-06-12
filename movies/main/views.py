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


# Create your views here.


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


# class IndexView(TemplateView):
#     template_name = 'main/index.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_profile = UserProfile.objects.get(user=self.request.user)
#         user_genres = user_profile.genres.all()
#         films = Film.objects.all()
#         films_on_genre = films.filter(genre__in=user_genres)[:10]
#         context['films_on_genre'] = films_on_genre
#         context['films'] = Film.objects.all()[:10]
#         context['genres'] = Genre.objects.all()
#         context['show_genre_modal'] = self.request.session.pop('show_genre_modal', False)
#         return context

# class IndexView(TemplateView):
#     template_name = 'main/index.html'
#
#     # def get(self, request, *args, **kwargs):
#     #     user_profile = UserProfile.objects.get(user=request.user)
#     #     user_genres = user_profile.genres.all()
#     #     films_on_genre = Film.objects.filter(genre__in=user_genres)[:10]
#     #     films_on_rating = Film.objects.all()[:8]
#     #     films = Film.objects.all()[:10]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['films_lists'] = [
#             {
#                 'title': 'Эксклюзивно для Вас',
#                 'scrolling': 'exclusive',
#                 'films':  Film.objects.all()[:10]
#             },
#             {
#                 'title': 'Другие фильмы',
#                 'scrolling': 'other',
#                 'films': Film.objects.all()[:8]  # Ваша фильтрация или запрос для другого скроллинга
#             },
#             # Добавьте остальные скроллинги в аналогичном формате
#             {
#                 'title': 'Новинки',
#                 'scrolling': 'new',
#                 'films': Film.objects.all()[:6]  # Ваша фильтрация или запрос для новинок
#             },
#             {
#                 'title': 'Рекомендации',
#                 'scrolling': 'recommendations',
#                 'films': Film.objects.all()[:4]  # Ваша фильтрация или запрос для рекомендаций
#             },
#         ]
#         context['show_genre_modal'] = self.request.session.pop('show_genre_modal', False)
#         return context

# class FilmDeatilView(DetailView):
#     model = Film
#     template_name = 'main/movie-detail.html'
#     context_object_name = 'film'

# class FilmDeatilView(DetailView):
#     model = Film
#     template_name = 'main/movie-detail.html'
#     context_object_name = 'film'
#
#     def post(self, request, *args, **kwargs):
#         film_id = self.kwargs['pk']
#         film = self.get_object()
#         is_viewed = request.POST.get('is_viewed')  # Получить значение checkbox из запроса
#         enrollment = Enrollment.objects.create(user=request.user.userprofile, film=film, isViewed=is_viewed)
#         # Дальнейшая обработка сохранения объекта Enrollment
#
#         return JsonResponse({'status': 'success'})  # Отправить успешный ответ в формате JSON

# class FilmDeatilView(DetailView):
#     model = Film
#     template_name = 'main/movie-detail.html'
#     context_object_name = 'film'
#
#     def post(self, request, slug):
#         film = self.get_object()
#         is_viewed = request.POST.get('is_viewed')  # Получить значение checkbox из запроса
#         enrollment = Enrollment.objects.create(user=request.user.userprofile, film=film, isViewed=is_viewed)
#         # Дальнейшая обработка сохранения объекта Enrollment
#
#         return JsonResponse({'status': 'success'})  # Отправить успешный ответ в формате JSON

class FilmDeatilView(DetailView):
    model = Film
    template_name = 'main/movie-detail.html'
    context_object_name = 'film'

    def post(self, request, slug):
        film = self.get_object()
        is_viewed = request.POST.get('is_viewed') == 'true'  # Преобразовать значение checkbox в тип bool

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

# class FilmDeatilView(DetailView):
#     model = Film
#     template_name = 'main/movie-detail.html'
#     context_object_name = 'film'
#
#     def post(self, request, slug):
#         film = self.get_object()
#         is_viewed = request.POST.get('is_viewed')  # Получить значение checkbox из запроса
#
#         # Проверить наличие записи Enrollment для данного фильма и пользователя
#         enrollment, created = Enrollment.objects.get_or_create(user=request.user.userprofile, film=film)
#         enrollment.isViewed = is_viewed  # Обновить значение поля isViewed
#         enrollment.save()
#
#         return JsonResponse({'status': 'success'})  # Отправить успешный ответ в формате JSON


# class MovieSelection(ListView):
#     model = Film
#     template_name = 'main/movies-selection.html'
#     context_object_name = 'films'
#     paginate_by = 10  # Количество фильмов на одной странице
#
#     def get_queryset(self):
#         scrolling = self.kwargs.get('scrolling')
#         if scrolling == 'exclusive':
#             queryset = Film.objects.all()[:10]
#         elif scrolling == 'other':
#             queryset = Film.objects.all()[:8]  # Ваша фильтрация или запрос для другого скроллинга
#         elif scrolling == 'new':
#             queryset = Film.objects.all()[:6]  # Ваша фильтрация или запрос для новинок
#         elif scrolling == 'recommendations':
#             queryset = Film.objects.all()[:4] # Ваша фильтрация или запрос для рекомендаций
#         else:
#             queryset = Film.objects.none()  # Пустой QuerySet, если скроллинг не определен
#         return queryset

class MovieSelection(ListView):
    model = Film
    template_name = 'main/movies-selection.html'
    context_object_name = 'films'
    queryset = Film.objects.all()[:10]



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
    genres = Genre.objects.all()
    years = Film.objects.values_list('year', flat=True).distinct()

    data = {
        'genres': genres,
        'years': years
    }

    return render(request, 'main/movies-rec.html', data)

# def index(request):
#     # create_genre()
#     # create_actors()
#     # create_directors()
#     # create_countries()
#     # create_films()
#     # setup_film_links()
#     # create_slugs()
#     #walk()
#     films = Film.objects.all()[:10]
#     return render(request, 'main/index.html', {'films': films})

# class IndexView(ListView):
#     template_name = 'main/index.html',
#     model = Film  # Модель, из которой будут получены объекты
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['genres'] = Genre.objects.all()  # Запрос к жанрам из базы данных
#     #     context['show_genre_modal'] = self.request.session.pop('show_genre_modal', False)
#     #     return context

def about(request):
    return render(request, 'main/about.html')

def movies(request):

    return render(request, 'main/movies.html')

# def movie_detail(request, title):
#     film = get_object_or_404(Film, title=title)
#     context = {'film': film}
#     return render(request, 'main/movie-detail.html', context)

def movies_rec(request):
    genres = Genre.objects.all().order_by('name')
    films = Film.objects.all()
    years = Film.objects.values_list('year', flat=True).distinct().order_by('-year')
    return render(request, 'main/movies-rec.html', {'genres': genres, 'films': films, 'years': years})


# def register(request):
#     return render(request, 'main/register.html')

def create_slugs():
    films = Film.objects.all()
    for film in films:
        film.slug = slugify(film.title)
        # film.save()

def create_genre():
    if Genre.objects.all().count() == 0:
        Genre.objects.create(name="Комедия")
        Genre.objects.create(name="Мультфилм")
        Genre.objects.create(name="Ужасы")
        Genre.objects.create(name="Фантастика")
        Genre.objects.create(name="Триллер")
        Genre.objects.create(name="Боевик")
        Genre.objects.create(name="Мелодрама")
        Genre.objects.create(name="Детектив")
        Genre.objects.create(name="Приключения")
        Genre.objects.create(name="Фэнтези")
        Genre.objects.create(name="Военный")
        Genre.objects.create(name="Документальный")
        Genre.objects.create(name="Детский")
        Genre.objects.create(name="Криминал")
        Genre.objects.create(name="Биография")
        Genre.objects.create(name="Вестерн")
        Genre.objects.create(name="Спортивный")
        Genre.objects.create(name="Мьюзикл")
    if Genre.objects.all().count() == 18:
        Genre.objects.create(name="Драма")

def create_actors():
    if Actor.objects.all().count() == 0:
        Actor.objects.create(name="Леонардо", surname="ДиКаприо")
        Actor.objects.create(name="Джона", surname="Хилл")
        Actor.objects.create(name="Марго", surname="Робби")
        Actor.objects.create(name="Кайл", surname="Чандлер")
        Actor.objects.create(name="Роб", surname="Райнер")
        Actor.objects.create(name="П.Дж", surname="Бирн")
        Actor.objects.create(name="Джон", surname="Бернтал")
        Actor.objects.create(name="Кристин", surname="Милиоти")
        Actor.objects.create(name="Жан", surname="Дюжарден")
        Actor.objects.create(name="Мэттью", surname="МакКонахи") ## волк с уолл стрит
        Actor.objects.create(name="Том", surname="Хэнкс")
        Actor.objects.create(name="Кристофер", surname="Уокен")
        Actor.objects.create(name="Мартин", surname="Шин")
        Actor.objects.create(name="Натали", surname="Бай")
        Actor.objects.create(name="Эми", surname="Адамс")
        Actor.objects.create(name="Джеймс", surname="Бролин")
        Actor.objects.create(name="Брайан", surname="Хау")
        Actor.objects.create(name="Стив", surname="Истин")
        Actor.objects.create(name="Джонни", surname=" Депп")
        Actor.objects.create(name="Кристиан", surname="Бэйл")
        Actor.objects.create(name="Марион", surname="Котийяр")
        Actor.objects.create(name="Стивен", surname="Лэнг")
        Actor.objects.create(name="Джейсон", surname="Кларк")
        Actor.objects.create(name="Стивен", surname="Грэм")
        Actor.objects.create(name="Билли", surname="Крудап")
        Actor.objects.create(name="Джон", surname="Ортис")
        Actor.objects.create(name="Бранка", surname="Катич")
        Actor.objects.create(name="Стивен", surname="Дорфф")
        Actor.objects.create(name="Кристиан", surname="Бэйл")
        Actor.objects.create(name="Стив", surname="Карелл")
        Actor.objects.create(name="Райан", surname="Гослинг")
        Actor.objects.create(name="Брэд", surname="Питт")
        Actor.objects.create(name="Мелисса", surname="Лео")
        Actor.objects.create(name="Хэмиш", surname="Линклейтер")
        Actor.objects.create(name="Джон", surname="Магаро")
        Actor.objects.create(name="Рейф", surname="Сполл")
        Actor.objects.create(name="Джереми", surname="Стронг")
        Actor.objects.create(name="Мариса", surname="Томей")
        Actor.objects.create(name="Мэтт", surname="Дэймон")
        Actor.objects.create(name="Гильфи", surname="Зога")
        Actor.objects.create(name="Андри", surname="Магнассон")
        Actor.objects.create(name="Сигридур", surname="Бенедиктсдоттир")
        Actor.objects.create(name="Пол", surname="Волкер")
        Actor.objects.create(name="Доминик", surname="Стросс-Кан")
        Actor.objects.create(name="Жорж", surname="Соррос")
        Actor.objects.create(name="Барни", surname="Фрэнк")
        Actor.objects.create(name="Дэвид", surname="МакКормик")
        Actor.objects.create(name="Скотт", surname="Тэлботт")
        Actor.objects.create(name="Джессика", surname="Честейн")
        Actor.objects.create(name="Идрис", surname="Эльба")
        Actor.objects.create(name="Кевин", surname="Костнер")
        Actor.objects.create(name="Майкл", surname="Сера")
        Actor.objects.create(name="Джереми", surname="Стронг")
        Actor.objects.create(name="Дж.С", surname="МакКензи")
        Actor.objects.create(name="Билл", surname="Кэмп")
        Actor.objects.create(name="Грэм", surname="Грин")
        Actor.objects.create(name="Том", surname="Хэнкс")
        Actor.objects.create(name="Дэвид", surname="Морс")
        Actor.objects.create(name="Бонни", surname="Хант")
        Actor.objects.create(name="Майкл", surname="Дункан")
        Actor.objects.create(name="Майкл", surname="Джитер")
        Actor.objects.create(name="Джеймс", surname="Кромуэлл")
        Actor.objects.create(name="Грэм", surname="Грин")
        Actor.objects.create(name="Даг", surname="Хатчисон")
        Actor.objects.create(name="Сэм", surname="Рокуэлл")
        Actor.objects.create(name="Барри", surname="Пеппер")
        Actor.objects.create(name="Тим", surname="Роббинс")
        Actor.objects.create(name="Морган", surname="Фриман")
        Actor.objects.create(name="Боб", surname="Гантон")
        Actor.objects.create(name="Уильям", surname="Сэдлер")
        Actor.objects.create(name="Клэнси", surname="Браун")
        Actor.objects.create(name="Гил", surname="Беллоуз")
        Actor.objects.create(name="Марк", surname="Ролстон")
        Actor.objects.create(name="Джеймс", surname="Уитмор")
        Actor.objects.create(name="Джеффри", surname="ДеМанн")
        Actor.objects.create(name="Ларри", surname="Бранденбург")
        Actor.objects.create(name="Робин", surname="Райт")
        Actor.objects.create(name="Салли", surname="Филд")
        Actor.objects.create(name="Гэри", surname="Синиз")
        Actor.objects.create(name="Майкелти", surname="Уильямсон")
        Actor.objects.create(name="Майкл", surname="Хэмпфри")
        Actor.objects.create(name="Сэм", surname="Андерсон")
        Actor.objects.create(name="Шиван", surname="Фэллон")
        Actor.objects.create(name="Ребекка", surname="Уильямс")
        Actor.objects.create(name="Энтони", surname="Гонсалес") ## тайна коко по 4 актера
        Actor.objects.create(name="Гаэль", surname="Берналь")
        Actor.objects.create(name="Бенджамин", surname="Брэтт")
        Actor.objects.create(name="Аланна", surname="Юбак")
        Actor.objects.create(name="Элайджа", surname="Вуд")
        Actor.objects.create(name="Вигго", surname="Мортенсен")
        Actor.objects.create(name="Шон", surname="Эстин")
        Actor.objects.create(name="Иэн", surname="Маккеллен")
        Actor.objects.create(name="Энн", surname="Хэтэуэй")
        Actor.objects.create(name="Маккензи", surname="Фой")
        Actor.objects.create(name="Эдвард", surname="Нортон")
        Actor.objects.create(name="Хелена", surname="Картер")
        Actor.objects.create(name="Мит", surname="Лоаф")
        Actor.objects.create(name="Мэттью", surname="Бродерик")
        Actor.objects.create(name="Джереми", surname="Айронс")
        Actor.objects.create(name="Нэйтан", surname="Лейн")
        Actor.objects.create(name="Эрни", surname="Сабелла")
        Actor.objects.create(name="Майк", surname="Майерс")
        Actor.objects.create(name="Эдди", surname="Мерфи")
        Actor.objects.create(name="Кэмерон", surname="Диас")
        Actor.objects.create(name="Джон", surname="Литгоу")
        Actor.objects.create(name="Марк", surname="Руффало")
        Actor.objects.create(name="Бен", surname="Кингсли")
        Actor.objects.create(name="Мишель", surname="Уильямс")
        Actor.objects.create(name="Евгений", surname="Леонов")
        Actor.objects.create(name="Георгий", surname="Вицин")
        Actor.objects.create(name="Раднэр", surname="Муратов")
        Actor.objects.create(name="Савелий", surname="Крамаров")
        Actor.objects.create(name="Маколей", surname="Калкин")
        Actor.objects.create(name="Джо", surname="Пеши")
        Actor.objects.create(name="Дэниел", surname="Стерн")
        Actor.objects.create(name="Джон", surname="Хёрд")
        Actor.objects.create(name="Джейсон", surname="Стэйтем")
        Actor.objects.create(name="Алан", surname="Форд")
        Actor.objects.create(name="Ричард", surname="Гир")
        Actor.objects.create(name="Джоан", surname="Аллен")
        Actor.objects.create(name="Сара", surname="Ремер")
        Actor.objects.create(name="Джейсон", surname="Александер")
        Actor.objects.create(name="Сергей", surname="Бодров")
        Actor.objects.create(name="Виктор", surname="Сухоруков")
        Actor.objects.create(name="Светлана", surname="Письмиченко")
        Actor.objects.create(name="Мария", surname="Милютина")
        Actor.objects.create(name="Сергей", surname="Маковецкий")
        Actor.objects.create(name="Ирина", surname="Салтыкова")
        Actor.objects.create(name="Джей", surname="Барушель")
        Actor.objects.create(name="Джерард", surname="Батлер")
        Actor.objects.create(name="Крэйг", surname="Фергюсон")
        Actor.objects.create(name="Америка", surname="Феррера")
        Actor.objects.create(name="Джули", surname="Эндрюс")
        Actor.objects.create(name="Орландо", surname="Блум")
        Actor.objects.create(name="Кира", surname="Найтли")
        Actor.objects.create(name="Джек", surname="Девенпорт")


def create_directors():
    if Director.objects.all().count() == 0:
        Director.objects.create(name="Мартин", surname="Скорсезе")
        Director.objects.create(name="Стивен", surname="Спилберг")
        Director.objects.create(name="Майкл", surname="Манн")
        Director.objects.create(name="Адам", surname="Маккей")
        Director.objects.create(name="Чарльз", surname="Фергюсон")
        Director.objects.create(name="Аарон", surname="Соркин")
        Director.objects.create(name="Фрэнк", surname="Дарабонт")
        Director.objects.create(name="Роберт", surname="Земекис")
        Director.objects.create(name="Эдриан", surname="Молина")
        Director.objects.create(name="Ли", surname="Анкрич")
        Director.objects.create(name="Питер", surname="Джексон")
        Director.objects.create(name="Кристофер", surname="Нолан")
        Director.objects.create(name="Дэвид", surname="Финчер")
        Director.objects.create(name="Роб", surname="Минкофф")
        Director.objects.create(name="Роджер", surname="Аллерс")
        Director.objects.create(name="Вики", surname="Дженсон")
        Director.objects.create(name="Эндрю", surname="Адамсон")
        Director.objects.create(name="Александр", surname="Серый")
        Director.objects.create(name="Крис", surname="Коламбус")
        Director.objects.create(name="Гай", surname="Ричи")
        Director.objects.create(name="Лассе", surname="Халльстрём")
        Director.objects.create(name="Алексей", surname="Балабанов")
        Director.objects.create(name="Крис", surname="Сандерс")
        Director.objects.create(name="Дин", surname="ДеБлуа")
        Director.objects.create(name="Келли", surname="Эсбёри")
        Director.objects.create(name="Конрад", surname="Вернон")
        Director.objects.create(name="Гор", surname="Вербински")

def create_countries():
    if Country.objects.all().count() == 0:
        Country.objects.create(name="США")
        Country.objects.create(name="Канада")
        Country.objects.create(name="Япония")
        Country.objects.create(name="Китай")
        Country.objects.create(name="Новая Зеландия")
        Country.objects.create(name="Великобритания")
        Country.objects.create(name="Германия")
        Country.objects.create(name="Швеция")
        Country.objects.create(name="СССР")
        Country.objects.create(name="Россия")
        Country.objects.create(name="Франция")

def walk():
    film = Film.objects.create(title="Волк с Уолл-стрит", year=2013, rating=8.0, description="1987 год. Джордан Белфорт становится брокером в успешном инвестиционном банке. Вскоре банк закрывается после внезапного обвала индекса Доу-Джонса. По совету жены Терезы Джордан устраивается в небольшое заведение, занимающееся мелкими акциями. Его настойчивый стиль общения с клиентами и врождённая харизма быстро даёт свои плоды. Он знакомится с соседом по дому Донни, торговцем, который сразу находит общий язык с Джорданом и решает открыть с ним собственную фирму. В качестве сотрудников они нанимают нескольких друзей Белфорта, его отца Макса и называют компанию «Стрэттон Оукмонт». В свободное от работы время Джордан прожигает жизнь: лавирует от одной вечеринки к другой, вступает в сексуальные отношения с проститутками, употребляет множество наркотических препаратов, в том числе кокаин и кваалюд. Однажды наступает момент, когда быстрым обогащением Белфорта начинает интересоваться агент ФБР...", poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/c5876e81-9dec-43e2-923f-fee2fca85e21/3840x")
    fant = Genre.objects.get(name="Фэнтези")
    boev = Genre.objects.get(name="Боевик")
    pric = Genre.objects.get(name="Приключения")

    film.genre.add(fant)
    film.genre.add(boev)
    film.genre.add(pric)

    actor1 = Actor.objects.get(name="Леонардо", surname="ДиКаприо")
    actor2 = Actor.objects.get(name="Джона", surname="Хилл")
    actor3 = Actor.objects.get(name="Марго", surname="Робби")
    actor4 = Actor.objects.get(name="Кайл", surname="Чандлер")
    actor5 = Actor.objects.get(name="Роб", surname="Райнер")
    actor6 = Actor.objects.get(name="П.Дж", surname="Бирн")
    actor7 = Actor.objects.get(name="Джон", surname="Бернтал")
    actor8 = Actor.objects.get(name="Кристин", surname="Милиоти")
    actor9 = Actor.objects.get(name="Жан", surname="Дюжарден")
    actor10 = Actor.objects.get(name="Мэттью", surname="МакКонахи")

    film.actors.add(actor1)
    film.actors.add(actor2)
    film.actors.add(actor3)
    film.actors.add(actor4)
    film.actors.add(actor5)
    film.actors.add(actor6)
    film.actors.add(actor7)
    film.actors.add(actor8)
    film.actors.add(actor9)
    film.actors.add(actor10)

    director = Director.objects.get(name="Мартин", surname="Скорсезе")

    film.directors.add(director)



def create_films():
    if Film.objects.all().count() == 1:
        Film.objects.create(title="Поймай меня, если сможешь", year=2002, rating=8.5,
                            description="Фрэнк Эбегнейл успел поработать врачом, адвокатом и пилотом на пассажирской авиалинии – и все это до достижения полного совершеннолетия в 21 год. Мастер в обмане и жульничестве, он также обладал искусством подделки документов, что в конечном счете принесло ему миллионы долларов, которые он получил по фальшивым чекам. Агент ФБР Карл Хэнрэтти отдал бы все, чтобы схватить Фрэнка и привлечь к ответственности за свои деяния, но Фрэнк всегда опережает его на шаг, заставляя продолжать погоню",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/b83da067-1e79-48e5-877d-d2ec87c0d2eb/576x")
        Film.objects.create(title="Джонни Д.", year=2009, rating=7.1,
                            description="Америка, 1930-е годы. Дерзкие нападения сделали Джона Диллинджера героем всех угнетённых и главной мишенью для лучшего агента Мелвина Первиса и директора Бюро расследований Джона Эдгара Гувера. Никто не мог остановить банду Диллинджера. Ни одна тюрьма не могла его удержать. В то время как приключения лихой банды, к которой примкнули Малыш Нельсон и Элвин Карпис, вдохновляют обозлённых граждан, Гувер решает воспользоваться случаем и превратить Бюро расследований в главную правоохранительную организацию страны - ФБР.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/e36fc8aa-ff04-4005-8872-c701aef087c1/600x900")
        Film.objects.create(title="Игра на понижение", year=2015, rating=7.4,
                            description="2005 год. Изучая данные ипотек по стране, чудаковатый финансовый гений и управляющий хедж-фонда Scion Capital Майкл Бьюрри обращает внимание на одну деталь и приходит к выводу, что американский рынок ипотечных кредитов может скоро лопнуть. В связи с этим он страхует около миллиарда долларов своих клиентов через кредитный дефолтный своп. Клиенты фонда Бьюрри волнуются из-за возможных потерь, ведь рынок ипотечных кредитов представляется весьма стабильным, но Майкл твёрдо стоит на своём. Вскоре эту странную активность замечают несколько финансистов на Уолл-стрит. Изучив данные, они осознают, что опасения Бьюрри имеют под собой веские основания. Более того, сыграв на понижение, можно заработать миллионы.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/7a48d968-4e6a-43b7-95f9-e47e5a9eecc1/600x900")
        Film.objects.create(title="Инсайдеры", year=2010, rating=7.7,
                            description="Спад в мировой экономике, убыток от которого был оценен в 20 триллионов долларов, повлек за собой потерю работы и жилья для нескольких миллионов человек. В ходе тщательных исследований и интервью с ведущими фигурами финансового мира, политическими деятелями и журналистами, фильм приоткрывает перед нами страшную правду о зарождении преступной индустрии и о ее сетях, позволивших подкупить политику, органы экономического регулирования и ученый мир…",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/4716873/d58e6c70-848a-4fef-bc30-e4b9bdf560be/600x900")
        Film.objects.create(title="Большая игра", year=2017, rating=7.7,
                            description="После очередной травмы могулистка Молли Блум решает завязать со спортом и пожить обычной жизнью. Так получается, что девушка сначала работает хостесс на нелегальных покерных играх, а вскоре и сама становится организатором подпольного казино для знаменитостей, миллионеров, членов королевских семей и других любителей в мгновение ока спустить целое состояние.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1900788/eabf413e-b465-4857-a7b0-9c54c260778f/600x900")
        Film.objects.create(title="Зеленая миля", year=1999, rating=9.1,
                            description="Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора», каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/4057c4b8-8208-4a04-b169-26b0661453e3/600x900")
        Film.objects.create(title="Побег из Шоушенка", year=1994, rating=9.1,
                            description="Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/0b76b2a2-d1c7-4f04-a284-80ff7bb709a4/600x900")
        Film.objects.create(title="Форрест Гамп", year=1994, rating=8.9,
                            description="Сидя на автобусной остановке, Форрест Гамп — не очень умный, но добрый и открытый парень — рассказывает случайным встречным историю своей необыкновенной жизни. С самого малолетства парень страдал от заболевания ног, соседские мальчишки дразнили его, но в один прекрасный день Форрест открыл в себе невероятные способности к бегу. Подруга детства Дженни всегда его поддерживала и защищала, но вскоре дороги их разошлись.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/3560b757-9b95-45ec-af8c-623972370f9d/600x900")
        Film.objects.create(title="Тайна Коко", year=2017, rating=8.7,
                            description="12-летний Мигель живёт в мексиканской деревушке в семье сапожников и тайно мечтает стать музыкантом. Тайно, потому что в его семье музыка считается проклятием. Когда-то его прапрадед оставил жену, прапрабабку Мигеля, ради мечты, которая теперь не даёт спокойно жить и его праправнуку. С тех пор музыкальная тема в семье стала табу. Мигель обнаруживает, что между ним и его любимым певцом Эрнесто де ла Крусом, ныне покойным, существует некая связь. Паренёк отправляется к своему кумиру в Страну Мёртвых, где встречает души предков. Мигель знакомится там с духом-скелетом по имени Гектор, который становится его проводником. Вдвоём они отправляются на поиски де ла Круса.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/6e11a16e-c9e7-491f-9162-01098a7d8dd9/600x900")
        Film.objects.create(title="Властелин колец: Возвращение короля", year=2003, rating=8.7,
                            description="Повелитель сил тьмы Саурон направляет свою бесчисленную армию под стены Минас-Тирита, крепости Последней Надежды. Он предвкушает близкую победу, но именно это мешает ему заметить две крохотные фигурки — хоббитов, приближающихся к Роковой Горе, где им предстоит уничтожить Кольцо Всевластья.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/e410c71f-baa1-4fe5-bb29-aedb4662f49b/600x900")
        Film.objects.create(title="Интерстеллар", year=2014, rating=8.6,
                            description="Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1600647/430042eb-ee69-4818-aed0-a312400a26bf/600x900")
        Film.objects.create(title="Бойцовский клуб", year=1999, rating=8.7,
                            description="Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Однажды в очередной командировке он встречает некоего Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. Тайлер уверен, что самосовершенствование — удел слабых, а единственное, ради чего стоит жить, — саморазрушение. Проходит немного времени, и вот уже новые друзья лупят друг друга почем зря на стоянке перед баром, и очищающий мордобой доставляет им высшее блаженство. Приобщая других мужчин к простым радостям физической жестокости, они основывают тайный Бойцовский клуб, который начинает пользоваться невероятной популярностью.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1898899/8ef070c9-2570-4540-9b83-d7ce759c0781/600x900")
        Film.objects.create(title="Властелин колец: Братство Кольца", year=2001, rating=8.6,
                            description="Сказания о Средиземье — это хроника Великой войны за Кольцо, длившейся не одну тысячу лет. Тот, кто владел Кольцом, получал неограниченную власть, но был обязан служить злу.Тихая деревня, где живут хоббиты. Придя на 111-й день рождения к своему старому другу Бильбо Бэггинсу, волшебник Гэндальф начинает вести разговор о кольце, которое Бильбо нашел много лет назад. Это кольцо принадлежало когда-то темному властителю Средиземья Саурону, и оно дает большую власть своему обладателю. Теперь Саурон хочет вернуть себе власть над Средиземьем. Бильбо отдает Кольцо племяннику Фродо, чтобы тот отнёс его к Роковой Горе и уничтожил.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/a2d5bcae-a1a9-442f-8195-f5373a5ba77f/600x900")
        Film.objects.create(title="Властелин колец: Две крепости", year=2002, rating=8.6,
                            description="Братство распалось, но Кольцо Всевластья должно быть уничтожено. Фродо и Сэм вынуждены довериться Голлуму, который взялся провести их к вратам Мордора. Громадная армия Сарумана приближается: члены братства и их союзники готовы принять бой. Битва за Средиземье продолжается.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/772093e4-7f68-49aa-a805-d654693aee26/600x900")
        Film.objects.create(title="Король Лев", year=1994, rating=8.8,
                            description="У величественного Короля-Льва Муфасы рождается наследник по имени Симба. Уже в детстве любознательный малыш становится жертвой интриг своего завистливого дяди Шрама, мечтающего о власти. Симба познаёт горе утраты, предательство и изгнание, но в конце концов обретает верных друзей и находит любимую. Закалённый испытаниями, он в нелёгкой борьбе отвоёвывает своё законное место в «Круге жизни», осознав, что значит быть настоящим Королём.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1704946/60aa1abc-b754-4817-ad9c-0bcda427a12b/600x900")
        Film.objects.create(title="Шрэк", year=2001, rating=8.1,
                            description="Жил да был в сказочном государстве большой зеленый великан по имени Шрэк. Жил он в гордом одиночестве в лесу, на болоте, которое считал своим. Но однажды злобный коротышка — лорд Фаркуад, правитель волшебного королевства, безжалостно согнал на Шрэково болото всех сказочных обитателей. И беспечной жизни зеленого великана пришел конец. Но лорд Фаркуад пообещал вернуть Шрэку болото, если великан добудет ему прекрасную принцессу Фиону, которая томится в неприступной башне, охраняемой огнедышащим драконом.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/7ade06a8-4178-4386-9ee2-87fec5a172eb/600x900")
        Film.objects.create(title="Остров проклятых", year=2009, rating=8.5,
                            description="Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/617303b7-cfa7-4273-bd1d-63974bf68927/600x900")
        Film.objects.create(title="Джентльмены удачи", year=1971, rating=8.5,
                            description="Заведующему детсадом Трошкину фатально не повезло: он оказался как две капли воды похож на бандита по кличке «Доцент», похитившего уникальный шлем Александра Македонского. Милиция внедряет добряка Трошкина в воровскую среду - и ему ничего не остается, кроме как старательно изображать своего двойника-злодея, путая всех окружающих. Со временем он настолько блестяще входит в роль, что сам начинает порой приходить в ужас. Между тем, жизни его угрожает смертельная опасность...",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1946459/218102a7-96be-4d7e-8029-815de0f37cfa/600x900")
        Film.objects.create(title="Один дома", year=1990, rating=8.3,
                            description="Американское семейство отправляется из Чикаго в Европу, но в спешке сборов бестолковые родители забывают дома... одного из своих детей. Юное создание, однако, не теряется и демонстрирует чудеса изобретательности. И когда в дом залезают грабители, им приходится не раз пожалеть о встрече с милым крошкой.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/6201401/022a58e3-5b9b-411b-bfb3-09fedb700401/600x900")
        Film.objects.create(title="Один дома 2: Затерянный в Нью-Йорке", year=1992, rating=8.0,
                            description="Самый маленький герой Америки устраивает большой переполох в Нью-Йорке! Кевин МакКалистер вернулся! Но теперь он один не дома, а в Нью-Йорке и у него достаточно денег и кредитных карточек, чтобы превратить Большое Яблоко в собственную площадку для игр.Но, как всегда, Кевину не суждено быть долго одному: его старые приятели ― жулики Гарри и Марв ― сбежали из тюрьмы, куда они попали стараниями Кевина. И надо же им было попасть именно в тот город, где Кевин планировал поразвлечься! Новые западни и ловушки уже ждут горе-бандитов.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/e87b5842-3065-422e-81e8-59a1ffcd9b6a/600x900")
        Film.objects.create(title="Большой куш", year=2000, rating=8.5,
                            description="Фрэнки Четыре Пальца должен был переправить краденый алмаз из Англии в США своему боссу Эви, но, сделав ставку на подпольный боксерский поединок, он попал в круговорот весьма нежелательных событий. Вокруг него и его груза разворачивается сложная интрига с участием множества колоритных персонажей лондонского дна — русского гангстера, троих незадачливых грабителей, хитрого боксера и угрюмого громилы грозного мафиози. Каждый норовит в одиночку сорвать большой куш.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/4303601/47fe48f6-ff17-4411-a12f-d337bea2639d/600x900")
        Film.objects.create(title="Хатико: Самый верный друг", year=2008, rating=8.4,
                            description="Однажды, возвращаясь с работы, профессор колледжа нашел на вокзале симпатичного щенка породы акита-ину. Профессор и Хатико стали верными друзьями. Каждый день пес провожал и встречал хозяина на вокзале.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1629390/82f8a2dc-a439-4832-9f0f-dc599e6e78d2/600x900")
        Film.objects.create(title="Брат", year=1997, rating=8.3,
                            description="Демобилизовавшись, Данила Багров вернулся в родной городок. Но скучная жизнь российской провинции не устраивала его, и он решился податься в Петербург, где, по слухам, уже несколько лет процветает его старший брат. Данила нашел брата. Но все оказалось не так просто — брат работает наемным убийцей.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1704946/e9008e2f-433f-43b0-b9b8-2ea8e3fb6c9b/600x900")
        Film.objects.create(title="Брат 2", year=2000, rating=8.2,
                            description="Участвуя в программе на телевидении, Данила Багров встречает своих друзей по службе в Чечне. Одного из них внезапно убивают. Выясняется, что у того были неприятности из-за брата-хоккеиста в Америке. Данила должен разобраться. Он вылетает в Америку и за компанию берёт с собой старшего брата.",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1704946/80eab631-346c-4c29-b14d-1fa1438158f9/600x900")
        Film.objects.create(title="Как приручить дракона", year=2010, rating=8.2,
                            description="Вы узнаете историю подростка Иккинга, которому не слишком близки традиции его героического племени, много лет ведущего войну с драконами. Мир Иккинга переворачивается с ног на голову, когда он неожиданно встречает дракона Беззубика, который поможет ему и другим викингам увидеть привычный мир с совершенно другой стороны…",
                            poster="https://www.kinopoisk.ru/film/280172/posters/")
        Film.objects.create(title="Шрэк 2", year=2004, rating=7.8,
                            description="Шрэк и Фиона возвращаются после медового месяца и находят письмо от родителей Фионы с приглашением на ужин. Однако те не подозревают, что их дочь тоже стала огром! Вместе с Осликом счастливая пара отправляется в путешествие, полное неожиданностей, и попадает в круговорот событий, во время которых приобретает множество друзей…",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1773646/27a3c989-e883-40f3-806f-f3ef27fe7177/600x900")
        Film.objects.create(title="Пираты Карибского моря: Сундук мертвеца", year=2006, rating=8.1,
                            description="Вновь оказавшись в ирреальном мире, лихой капитан Джек Воробей неожиданно узнает, что является должником легендарного капитана «Летучего Голландца» Дэйви Джонса. Джек должен в кратчайшие сроки решить эту проблему, иначе ему грозит вечное проклятие и рабское существование после смерти. Вдобавок ко всему, срывается свадьба Уилла Тернера и Элизабет Суонн, которые вынуждены составить Джеку компанию в его злоключениях…",
                            poster="https://avatars.mds.yandex.net/get-kinopoisk-image/1599028/2f896b6f-397e-40ef-ae19-e9cb0b2d9675/600x900")

def setup_film_links():

    comedy = Genre.objects.get(name="Комедия")
    mult = Genre.objects.get(name="Мультфилм")
    horror = Genre.objects.get(name="Ужасы")
    fantastic = Genre.objects.get(name="Фантастика")
    triller = Genre.objects.get(name="Триллер")
    boevik = Genre.objects.get(name="Боевик")
    melodrama = Genre.objects.get(name="Мелодрама")
    detectiv = Genre.objects.get(name="Детектив")
    pric = Genre.objects.get(name="Приключения")
    fantasy = Genre.objects.get(name="Фэнтези")
    voenn = Genre.objects.get(name="Военный")
    docum = Genre.objects.get(name="Документальный")
    det = Genre.objects.get(name="Детский")
    crim = Genre.objects.get(name="Криминал")
    bio = Genre.objects.get(name="Биография")
    vestern = Genre.objects.get(name="Вестерн")
    sport = Genre.objects.get(name="Спортивный")
    musicl = Genre.objects.get(name="Мьюзикл")
    drama = Genre.objects.get(name="Драма")
    history = Genre.objects.create(name="История")

    usa = Country.objects.get(name="США")
    canada = Country.objects.get(name="Канада")
    japan = Country.objects.get(name="Япония")
    china = Country.objects.get(name="Китай")
    new_zeland = Country.objects.get(name="Новая Зеландия")
    gb = Country.objects.get(name="Великобритания")
    germany = Country.objects.get(name="Германия")
    shw = Country.objects.get(name="Швеция")
    sssr = Country.objects.get(name="СССР")
    russia = Country.objects.get(name="Россия")
    france = Country.objects.get(name="Франция")


    director1 = Director.objects.get(name="Мартин", surname="Скорсезе")
    director2 = Director.objects.get(name="Стивен", surname="Спилберг")
    director3 = Director.objects.get(name="Майкл", surname="Манн")
    director4 = Director.objects.get(name="Адам", surname="Маккей")
    director5 = Director.objects.get(name="Чарльз", surname="Фергюсон")
    director6 = Director.objects.get(name="Аарон", surname="Соркин")
    director7 = Director.objects.get(name="Фрэнк", surname="Дарабонт")
    director8 = Director.objects.get(name="Роберт", surname="Земекис")
    director9 = Director.objects.get(name="Эдриан", surname="Молина")
    director10 = Director.objects.get(name="Ли", surname="Анкрич")
    director11 = Director.objects.get(name="Питер", surname="Джексон")
    director12 = Director.objects.get(name="Кристофер", surname="Нолан")
    director13 = Director.objects.get(name="Дэвид", surname="Финчер")
    director14 = Director.objects.get(name="Роб", surname="Минкофф")
    director15 = Director.objects.get(name="Роджер", surname="Аллерс")
    director16 = Director.objects.get(name="Вики", surname="Дженсон")
    director17 = Director.objects.get(name="Эндрю", surname="Адамсон")
    director18 = Director.objects.get(name="Александр", surname="Серый")
    director19 = Director.objects.get(name="Крис", surname="Коламбус")
    director20 = Director.objects.get(name="Гай", surname="Ричи")
    director21 = Director.objects.get(name="Лассе", surname="Халльстрём")
    director22 = Director.objects.get(name="Алексей", surname="Балабанов")
    director23 = Director.objects.get(name="Крис", surname="Сандерс")
    director24 = Director.objects.get(name="Дин", surname="ДеБлуа")
    director25 = Director.objects.get(name="Келли", surname="Эсбёри")
    director26 = Director.objects.get(name="Конрад", surname="Вернон")
    director27 = Director.objects.get(name="Гор", surname="Вербински")

    actor1 = Actor.objects.get(name="Леонардо", surname="ДиКаприо")
    actor2 = Actor.objects.get(name="Джона", surname="Хилл")
    actor3 = Actor.objects.get(name="Марго", surname="Робби")
    actor4 = Actor.objects.get(name="Кайл", surname="Чандлер")
    actor5 = Actor.objects.get(name="Роб", surname="Райнер")
    actor6 = Actor.objects.get(name="П.Дж", surname="Бирн")
    actor7 = Actor.objects.get(name="Джон", surname="Бернтал")
    actor8 = Actor.objects.get(name="Кристин", surname="Милиоти")
    actor9 = Actor.objects.get(name="Жан", surname="Дюжарден")
    actor10 = Actor.objects.get(name="Мэттью", surname="МакКонахи")
    actor11 = Actor.objects.get(name="Том", surname="Хэнкс")
    actor12 = Actor.objects.get(name="Кристофер", surname="Уокен")
    actor13 = Actor.objects.get(name="Мартин", surname="Шин")
    actor14 = Actor.objects.get(name="Натали", surname="Бай")
    actor15 = Actor.objects.get(name="Эми", surname="Адамс")
    actor16 = Actor.objects.get(name="Джеймс", surname="Бролин")
    actor17 = Actor.objects.get(name="Брайан", surname="Хау")
    actor18 = Actor.objects.get(name="Стив", surname="Истин")
    actor19 = Actor.objects.get(name="Джонни", surname=" Депп")
    actor20 = Actor.objects.get(name="Кристиан", surname="Бэйл")
    actor21 = Actor.objects.get(name="Марион", surname="Котийяр")
    actor22 = Actor.objects.get(name="Стивен", surname="Лэнг")
    actor23 = Actor.objects.get(name="Джейсон", surname="Кларк")
    actor24 = Actor.objects.get(name="Стивен", surname="Грэм")
    actor25 = Actor.objects.get(name="Билли", surname="Крудап")
    actor26 = Actor.objects.get(name="Джон", surname="Ортис")
    actor27 = Actor.objects.get(name="Бранка", surname="Катич")
    actor28 = Actor.objects.get(name="Стивен", surname="Дорфф")
    actor29 = Actor.objects.get(name="Кристиан", surname="Бэйл")
    actor30 = Actor.objects.get(name="Стив", surname="Карелл")
    actor31 = Actor.objects.get(name="Райан", surname="Гослинг")
    actor32 = Actor.objects.get(name="Брэд", surname="Питт")
    actor33 = Actor.objects.get(name="Мелисса", surname="Лео")
    actor34 = Actor.objects.get(name="Хэмиш", surname="Линклейтер")
    actor35 = Actor.objects.get(name="Джон", surname="Магаро")
    actor36 = Actor.objects.get(name="Рейф", surname="Сполл")
    actor37 = Actor.objects.get(name="Джереми", surname="Стронг")
    actor38 = Actor.objects.get(name="Мариса", surname="Томей")
    actor39 = Actor.objects.get(name="Мэтт", surname="Дэймон")
    actor40 = Actor.objects.get(name="Гильфи", surname="Зога")
    actor41 = Actor.objects.get(name="Андри", surname="Магнассон")
    actor42 = Actor.objects.get(name="Сигридур", surname="Бенедиктсдоттир")
    actor43 = Actor.objects.get(name="Пол", surname="Волкер")
    actor44 = Actor.objects.get(name="Доминик", surname="Стросс-Кан")
    actor45 = Actor.objects.get(name="Жорж", surname="Соррос")
    actor46 = Actor.objects.get(name="Барни", surname="Фрэнк")
    actor47 = Actor.objects.get(name="Дэвид", surname="МакКормик")
    actor48 = Actor.objects.get(name="Скотт", surname="Тэлботт")
    actor49 = Actor.objects.get(name="Джессика", surname="Честейн")
    actor50 = Actor.objects.get(name="Идрис", surname="Эльба")
    actor51 = Actor.objects.get(name="Кевин", surname="Костнер")
    actor52 = Actor.objects.get(name="Майкл", surname="Сера")
    actor53 = Actor.objects.get(name="Джереми", surname="Стронг")
    actor54 = Actor.objects.get(name="Дж.С", surname="МакКензи")
    actor55 = Actor.objects.get(name="Билл", surname="Кэмп")
    actor56 = Actor.objects.get(name="Грэм", surname="Грин")
    actor57 = Actor.objects.get(name="Том", surname="Хэнкс")
    actor58 = Actor.objects.get(name="Дэвид", surname="Морс")
    actor59 = Actor.objects.get(name="Бонни", surname="Хант")
    actor60 = Actor.objects.get(name="Майкл", surname="Дункан")
    actor61 = Actor.objects.get(name="Майкл", surname="Джитер")
    actor62 = Actor.objects.get(name="Джеймс", surname="Кромуэлл")
    actor63 = Actor.objects.get(name="Грэм", surname="Грин")
    actor64 = Actor.objects.get(name="Даг", surname="Хатчисон")
    actor65 = Actor.objects.get(name="Сэм", surname="Рокуэлл")
    actor66 = Actor.objects.get(name="Барри", surname="Пеппер")
    actor67 = Actor.objects.get(name="Тим", surname="Роббинс")
    actor68 = Actor.objects.get(name="Морган", surname="Фриман")
    actor69 = Actor.objects.get(name="Боб", surname="Гантон")
    actor70 = Actor.objects.get(name="Уильям", surname="Сэдлер")
    actor71 = Actor.objects.get(name="Клэнси", surname="Браун")
    actor72 = Actor.objects.get(name="Гил", surname="Беллоуз")
    actor73 = Actor.objects.get(name="Марк", surname="Ролстон")
    actor74 = Actor.objects.get(name="Джеймс", surname="Уитмор")
    actor75 = Actor.objects.get(name="Джеффри", surname="ДеМанн")
    actor76 = Actor.objects.get(name="Ларри", surname="Бранденбург")
    actor77 = Actor.objects.get(name="Робин", surname="Райт")
    actor78 = Actor.objects.get(name="Салли", surname="Филд")
    actor79 = Actor.objects.get(name="Гэри", surname="Синиз")
    actor80 = Actor.objects.get(name="Майкелти", surname="Уильямсон")
    actor81 = Actor.objects.get(name="Майкл", surname="Хэмпфри")
    actor82 = Actor.objects.get(name="Сэм", surname="Андерсон")
    actor83 = Actor.objects.get(name="Шиван", surname="Фэллон")
    actor84 = Actor.objects.get(name="Ребекка", surname="Уильямс")
    actor85 = Actor.objects.get(name="Энтони", surname="Гонсалес")
    actor86 = Actor.objects.get(name="Гаэль", surname="Берналь")
    actor87 = Actor.objects.get(name="Бенджамин", surname="Брэтт")
    actor88 = Actor.objects.get(name="Аланна", surname="Юбак")
    actor89 = Actor.objects.get(name="Элайджа", surname="Вуд")
    actor90 = Actor.objects.get(name="Вигго", surname="Мортенсен")
    actor91 = Actor.objects.get(name="Шон", surname="Эстин")
    actor92 = Actor.objects.get(name="Иэн", surname="Маккеллен")
    actor93 = Actor.objects.get(name="Энн", surname="Хэтэуэй")
    actor94 = Actor.objects.get(name="Маккензи", surname="Фой")
    actor95 = Actor.objects.get(name="Эдвард", surname="Нортон")
    actor96 = Actor.objects.get(name="Хелена", surname="Картер")
    actor97 = Actor.objects.get(name="Мит", surname="Лоаф")
    actor98 = Actor.objects.get(name="Мэттью", surname="Бродерик")
    actor99 = Actor.objects.get(name="Джереми", surname="Айронс")
    actor100 = Actor.objects.get(name="Нэйтан", surname="Лейн")
    actor101 = Actor.objects.get(name="Эрни", surname="Сабелла")
    actor102 = Actor.objects.get(name="Майк", surname="Майерс")
    actor103 = Actor.objects.get(name="Эдди", surname="Мерфи")
    actor104 = Actor.objects.get(name="Кэмерон", surname="Диас")
    actor105 = Actor.objects.get(name="Джон", surname="Литгоу")
    actor106 = Actor.objects.get(name="Марк", surname="Руффало")
    actor107 = Actor.objects.get(name="Бен", surname="Кингсли")
    actor108 = Actor.objects.get(name="Мишель", surname="Уильямс")
    actor109 = Actor.objects.get(name="Евгений", surname="Леонов")
    actor110 = Actor.objects.get(name="Георгий", surname="Вицин")
    actor111 = Actor.objects.get(name="Раднэр", surname="Муратов")
    actor112 = Actor.objects.get(name="Савелий", surname="Крамаров")
    actor113 = Actor.objects.get(name="Маколей", surname="Калкин")
    actor114 = Actor.objects.get(name="Джо", surname="Пеши")
    actor115 = Actor.objects.get(name="Дэниел", surname="Стерн")
    actor116 = Actor.objects.get(name="Джон", surname="Хёрд")
    actor117 = Actor.objects.get(name="Джейсон", surname="Стэйтем")
    actor118 = Actor.objects.get(name="Алан", surname="Форд")
    actor119 = Actor.objects.get(name="Ричард", surname="Гир")
    actor120 = Actor.objects.get(name="Джоан", surname="Аллен")
    actor121 = Actor.objects.get(name="Сара", surname="Ремер")
    actor122 = Actor.objects.get(name="Джейсон", surname="Александер")
    actor123 = Actor.objects.get(name="Сергей", surname="Бодров")
    actor124 = Actor.objects.get(name="Виктор", surname="Сухоруков")
    actor125 = Actor.objects.get(name="Светлана", surname="Письмиченко")
    actor126 = Actor.objects.get(name="Мария", surname="Милютина")
    actor127 = Actor.objects.get(name="Сергей", surname="Маковецкий")
    actor128 = Actor.objects.get(name="Ирина", surname="Салтыкова")
    actor129 = Actor.objects.get(name="Джей", surname="Барушель")
    actor130 = Actor.objects.get(name="Джерард", surname="Батлер")
    actor131 = Actor.objects.get(name="Крэйг", surname="Фергюсон")
    actor132 = Actor.objects.get(name="Америка", surname="Феррера")
    actor133 = Actor.objects.get(name="Джули", surname="Эндрюс")
    actor134 = Actor.objects.get(name="Орландо", surname="Блум")
    actor135 = Actor.objects.get(name="Кира", surname="Найтли")
    actor136 = Actor.objects.get(name="Джек", surname="Девенпорт")
    # ------------------------------------------------------------------------------------------------
    film1 = Film.objects.get(title="Волк с Уолл-стрит")
    film1.genre.add(drama, crim, bio, comedy)
    film1.country.add(usa)
    film1.directors.add(director1)
    film1.actors.add(actor1, actor2, actor3, actor4, actor5, actor6, actor7, actor8, actor9, actor10)
    # ------------------------------------------------------------------------------------------------
    film2 = Film.objects.get(title="Поймай меня, если сможешь")
    film2.genre.add(crim, bio, comedy)
    film2.country.add(usa, canada)
    film2.directors.add(director2)
    film2.actors.add(actor1, actor11, actor12, actor13, actor14, actor15, actor16, actor17, actor18)
    # ------------------------------------------------------------------------------------------------
    film3 = Film.objects.get(title="Джонни Д.")
    film3.genre.add(comedy, drama, history, bio)
    film3.country.add(usa)
    film3.directors.add(director3)
    film3.actors.add(actor19, actor20, actor21, actor22, actor23, actor24, actor25, actor26, actor27, actor28)
    # ------------------------------------------------------------------------------------------------
    film4 = Film.objects.get(title="Игра на понижение")
    film4.genre.add(crim, bio, comedy)
    film4.country.add(usa)
    film4.directors.add(director4)
    film4.actors.add(actor20, actor30, actor31, actor32, actor33, actor34, actor35, actor36, actor37, actor38)
    # ------------------------------------------------------------------------------------------------
    film5 = Film.objects.get(title="Инсайдеры")
    film5.genre.add(docum, crim)
    film5.country.add(usa)
    film5.directors.add(director5)
    film5.actors.add(actor39, actor40, actor41, actor42, actor43, actor44, actor45, actor46, actor47, actor48)
    # ------------------------------------------------------------------------------------------------
    film6 = Film.objects.get(title="Большая игра")
    film6.genre.add(bio, crim, drama)
    film6.country.add(usa, canada, china)
    film6.directors.add(director6)
    film6.actors.add(actor49, actor50, actor51, actor52, actor37, actor54, actor55, actor56)
    # ------------------------------------------------------------------------------------------------
    film9 = Film.objects.get(title="Зеленая миля")
    film9.genre.add(drama, fantasy, crim)
    film9.country.add(usa)
    film9.directors.add(director7)
    film9.actors.add(actor11, actor58, actor59, actor60, actor61, actor62, actor56, actor64, actor65, actor66)
    # ------------------------------------------------------------------------------------------------
    film10 = Film.objects.get(title="Побег из Шоушенка")
    film10.genre.add(drama)
    film10.country.add(usa)
    film10.directors.add(director7)
    film10.actors.add(actor67, actor68, actor69, actor70, actor71, actor72, actor73, actor74, actor75, actor76)
    # ------------------------------------------------------------------------------------------------
    film11 = Film.objects.get(title="Форрест Гамп")
    film11.genre.add(drama, comedy, melodrama, history, voenn)
    film11.country.add(usa)
    film11.directors.add(director8)
    film11.actors.add(actor11, actor77, actor78, actor79, actor80, actor81, actor82, actor83, actor84)
    # ------------------------------------------------------------------------------------------------
    film12 = Film.objects.get(title="Тайна Коко")
    film12.genre.add(mult, fantasy, comedy, pric)
    film12.country.add(usa, japan)
    film12.directors.add(director9, director10)
    film12.actors.add(actor85, actor86, actor87, actor88)
    # ------------------------------------------------------------------------------------------------
    film13 = Film.objects.get(title="Властелин колец: Возвращение короля")
    film13.genre.add(fantasy, pric, drama, boevik)
    film13.country.add(new_zeland, usa)
    film13.directors.add(director11)
    film13.actors.add(actor89, actor90, actor91, actor92)
    # ------------------------------------------------------------------------------------------------
    film14 = Film.objects.get(title="Интерстеллар")
    film14.genre.add(fantastic, drama, pric)
    film14.country.add(usa, gb, canada)
    film14.directors.add(director12)
    film14.actors.add(actor10, actor93, actor94)
    # ------------------------------------------------------------------------------------------------
    film15 = Film.objects.get(title="Бойцовский клуб")
    film15.genre.add(triller, drama, crim)
    film15.country.add(usa, germany)
    film15.directors.add(director13)
    film15.actors.add(actor95, actor32, actor96, actor97)
    # ------------------------------------------------------------------------------------------------
    film16 = Film.objects.get(title="Властелин колец: Братство Кольца")
    film16.genre.add(fantasy, pric, drama, boevik)
    film16.country.add(new_zeland, usa)
    film16.directors.add(director11)
    film16.actors.add(actor89, actor90, actor91, actor92)
    # ------------------------------------------------------------------------------------------------
    film17 = Film.objects.get(title="Властелин колец: Две крепости")
    film17.genre.add(fantasy, pric, drama, boevik)
    film17.country.add(new_zeland, usa)
    film17.directors.add(director11)
    film17.actors.add(actor89, actor90, actor91, actor92)
    # ------------------------------------------------------------------------------------------------
    film18 = Film.objects.get(title="Король Лев")
    film18.genre.add(mult, musicl, drama, pric)
    film18.country.add(usa)
    film18.directors.add(director14, director15)
    film18.actors.add(actor98, actor99, actor100, actor101)
    # ------------------------------------------------------------------------------------------------
    film19 = Film.objects.get(title="Шрэк")
    film19.genre.add(mult, fantasy, melodrama, comedy, pric)
    film19.country.add(usa, canada, shw)
    film19.directors.add(director16, director17)
    film19.actors.add(actor102, actor103, actor104, actor105)
    # ------------------------------------------------------------------------------------------------
    film20 = Film.objects.get(title="Остров проклятых")
    film20.genre.add(triller, detectiv, drama)
    film20.country.add(usa)
    film20.directors.add(director1)
    film20.actors.add(actor1, actor106, actor107, actor108)
    # ------------------------------------------------------------------------------------------------
    film21 = Film.objects.get(title="Джентльмены удачи")
    film21.genre.add(comedy, drama, crim, detectiv)
    film21.country.add(sssr)
    film21.directors.add(director18)
    film21.actors.add(actor109, actor110, actor111, actor112)
    # ------------------------------------------------------------------------------------------------
    film22 = Film.objects.get(title="Один дома")
    film22.genre.add(comedy)
    film22.country.add(usa)
    film22.directors.add(director19)
    film22. actors.add(actor113, actor114, actor115, actor116)
    # ------------------------------------------------------------------------------------------------
    film23 = Film.objects.get(title="Один дома 2: Затерянный в Нью-Йорке")
    film23.genre.add(comedy, pric)
    film23.country.add(usa)
    film23.directors.add(director19)
    film23.actors.add(actor113, actor114, actor115, actor116)
    # ------------------------------------------------------------------------------------------------
    film24 = Film.objects.get(title="Большой куш")
    film24.genre.add(crim, comedy, boevik)
    film24.country.add(gb, usa)
    film24.directors.add(director20)
    film24.actors.add(actor117, actor10, actor118)
    # ------------------------------------------------------------------------------------------------
    film25 = Film.objects.get(title="Хатико: Самый верный друг")
    film25.genre.add(drama, bio)
    film25.country.add(usa, gb)
    film25.directors.add(director21)
    film25.actors.add(actor119, actor120, actor121, actor122)
    # ------------------------------------------------------------------------------------------------
    film26 = Film.objects.get(title="Брат")
    film26.genre.add(drama, crim, boevik)
    film26.country.add(russia)
    film26.directors.add(director22)
    film26.actors.add(actor123, actor124, actor125, actor126)
    # ------------------------------------------------------------------------------------------------
    film27 = Film.objects.get(title="Брат 2")
    film27.genre.add(boevik, crim)
    film27.country.add(russia)
    film27.directors.add(director22)
    film27.actors.add(actor123, actor124, actor127, actor128)
    # ------------------------------------------------------------------------------------------------
    film28 = Film.objects.get(title="Как приручить дракона")
    film28.genre.add(mult, fantasy, comedy, pric)
    film28.country.add(usa, france)
    film28.directors.add(director23, director24)
    film28.actors.add(actor129, actor130, actor131, actor132)
    # ------------------------------------------------------------------------------------------------
    film29 = Film.objects.get(title="Шрэк 2")
    film29.genre.add(mult, fantasy, melodrama, comedy, pric)
    film29.country.add(usa, canada)
    film29.directors.add(director17, director25, director26)
    film29.actors.add(actor102,actor103, actor104, actor133)
    # ------------------------------------------------------------------------------------------------
    film30 = Film.objects.get(title="Пираты Карибского моря: Сундук мертвеца")
    film30.genre.add(fantasy, boevik, pric)
    film30.country.add(usa)
    film30.directors.add(director27)
    film30.actors.add(actor19, actor134, actor135, actor136)
























