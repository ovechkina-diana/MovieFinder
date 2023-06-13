from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views import View

from .models import UserProfile

from .forms import RegisterUserForm, LoginUserForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

#определяется класс представления RegisterUser для обработки регистрации новых пользователей
class RegisterUser(CreateView):
    # класс формы, который будет использоваться для отображения и обработки данных регистрации
    form_class = RegisterUserForm
    # шаблон HTML, который будет использоваться для отображения страницы регистрации
    template_name = 'user/register.html'
    # URL-адрес, на который будет перенаправлен пользователь после успешной регистрации
    success_url = reverse_lazy('main:profile')

    # переопределен для представления и добавляет дополнительные данные контекста в шаблон
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # значение переменной title в контексте, которое будет использовано в шаблоне
        context['title'] = "Регистрация"
        return context

    # переопределен для представления и вызывается при отправке валидной формы
    def form_valid(self, form):
        # создается новый пользователь на основе данных формы
        user = form.save()
        # аутентифицируется пользователь, входящий в систему
        login(self.request, user)
        # создается профиль пользователя (UserProfile) для нового пользователя
        UserProfile.objects.create(user=user)

        # устанавливается значение в сессии, чтобы показать модальное окно для выбора жанров пользователю
        self.request.session['show_genre_modal'] = True
        # перенаправляет пользователя на главную страницу после успешной регистрации
        return redirect('main:home')

    # переопределен для представления и возвращает URL-адрес, на который будет перенаправлен пользователь после успешной регистрации
    def get_success_url(self):
        return reverse_lazy('main:home')

# определяется класс представления LoginUser для обработки входа пользователей
class LoginUser(LoginView):
    # класс формы LoginUserForm, который будет использоваться для отображения и обработки данных входа пользователя
    form_class = LoginUserForm
    # шаблон HTML, который будет использоваться для отображения страницы входа
    template_name = 'user/login.html'

    # переопределен для представления и добавляет дополнительные данные контекста в шаблон
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # значение переменной title в контексте, которое будет использовано в шаблоне
        context['title'] = "Вход"
        return context

    # переопределен для представления и возвращает URL-адрес, на который будет перенаправлен пользователь после успешного входа
    def get_success_url(self):
        return reverse_lazy('main:home')

# обрабатка запроса для модального окна выбора жанров после регистрации пользователя
def genre_selection(request):
    # аутентифицирован ли пользователь и является ли метод запроса GET
    if request.user.is_authenticated and request.method == 'GET':
        # получаем значение параметра "genres" из GET-запроса
        genres = request.GET.get('genres')
        # создаем список genre_list, в который добавляются значения жанров из строки genres
        genre_list = [int(genre) for genre in genres.split(',')]
        # получаем профиль пользователя на основе текущего пользователя
        user_profile = UserProfile.objects.get(user=request.user)
        # Очищаем список жанров пользователя
        user_profile.genres.clear()
        # Добавляем выбранные жанры
        user_profile.genres.add(*genre_list)

        # Если условие не выполнено, то возвращается ответ "Method Not Allowed" с кодом состояния 405
        return HttpResponse('Success')
    else:
        return HttpResponse('Method Not Allowed', status=405)

# обработка запроса для выхода пользователя из системы
def logout_user(request):
    # Функция Django для выхода пользователя из системы
    logout(request)
    # аеренаправляем пользователя на страницу входа после успешного выход
    return redirect('user:login')

# обрабатка запроса для отображения профиля пользователя
def profile(request):
    # получаем объект профиля пользователя на основе текущего пользователя
    user_profile = UserProfile.objects.get(user=request.user)
    # получаем все жанры пользователя, связанные с его профилем
    user_genres = user_profile.genres.all()
    # получаем все фильмы, просмотренные пользователем, на основе связи через модел/таблицу Enrollment
    user_viewed_films = user_profile.films.filter(enrollment__isViewed=True)

    # возвращаем ответ с отображением шаблона и передачей словаря,
    # содержащего user_genres и user_viewed_films, в качестве контекста шаблона
    return render(request, 'user/profile.html', {'genres': user_genres, 'films': user_viewed_films})


