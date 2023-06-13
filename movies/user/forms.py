from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# определяется класс формы RegisterUserForm для регистрации новых пользователей
# наследуется от UserCreationForm - стандартной формы регистрации Django,
# которая обеспечивает функциональность регистрации пользователя
class RegisterUserForm(UserCreationForm):
    # Поле для ввода логина пользователя с меткой "Логин".
    # Используется виджет TextInput с CSS-классом "form-control" и атрибутом "placeholder" для отображения подсказки в поле ввода
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    # Поле для ввода электронной почты пользователя с меткой "Email".
    # Используется виджет EmailInput с CSS-классом "form-control", атрибутом "id" для идентификации элемента на странице и
    # атрибутом "placeholder" для отображения подсказки в поле ввода
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'register-email',
                                                            'placeholder': 'Введите ваш email'}))
    # Поле для ввода пароля пользователя с меткой "Пароль". Используется виджет PasswordInput с CSS-классом "form-control",
    # атрибутом "id" для идентификации элемента на странице и атрибутом "placeholder" для отображения подсказки в поле ввода
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register-password',
                                                                  'placeholder': 'Введите пароль'}))
    # Поле для повторного ввода пароля пользователя с меткой "Повтор пароля". Используется виджет PasswordInput
    # с CSS-классом "form-control", атрибутом "id" для идентификации элемента на странице и атрибутом "placeholder"
    # для отображения подсказки в поле ввода
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register-confirm-password',
                                                                                         'placeholder': 'Подтвердите пароль'}))
    # Внутренний класс, определяющий метаданные формы.
    # Указана модель User, к которой форма будет привязана, и перечислены поля, которые будут отображаться в форме
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# определяется класс формы LoginUserForm для аутентификации пользователей при входе в систему
# наследуется от AuthenticationForm - стандартной формы аутентификации Django,
# которая обеспечивает функциональность аутентификации пользователя
class LoginUserForm(AuthenticationForm):
    # Поле для ввода логина пользователя с меткой "Логин". Используется виджет TextInput с CSS-классом "form-control"
    # и атрибутом "placeholder" для отображения подсказки в поле ввода
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    # Поле для ввода пароля пользователя с меткой "Пароль". Используется виджет PasswordInput с CSS-классом "form-control",
    # атрибутом "id" для идентификации элемента на странице и атрибутом "placeholder" для отображения подсказки в поле ввода
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'login-password',
                                                                 'placeholder': 'Введите пароль'}))

