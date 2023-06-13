from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Genre, Film

# определяется модель/таблица UserProfile
class UserProfile(models.Model):
    # связь один к одному с моделью/таблицей User,
    # которое связывает профиль пользователя с соответствующей учетной записью пользователя
    # модель User предопределена в фреймворке Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # связь многие ко многим с таблицей Genre, создается дополнительная таблица, которая обеспечивает эту связь
    genres = models.ManyToManyField(Genre)
    # связь многие ко многим с таблицей Film, через таблицу Enrollment
    films = models.ManyToManyField(Film, through="Enrollment")

# определяется модель/таблица Enrollment
class Enrollment(models.Model):
    # Внешний ключ с моделью/таблицей UserProfile, который связывает запись просмотра с профилем пользователя
    user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    # Внешний ключ с моделью/таблицей Film, который связывает запись просмотра с фильмом
    film = models.ForeignKey(Film,  on_delete=models.CASCADE)
    # Булево поле, которое указывает, был ли фильм просмотрен пользователем. По умолчанию установлено значение False.
    isViewed = models.BooleanField(default=False)
