from django.db import models
from slugify import slugify
from django.urls import reverse


# ДАННЫЕ МОЕДИЛИ СОЗДАЮТ ТАБЛИЦЫ НА ОСНОВЕ МОДЕЛЕЙ В БД

# создание модели Actor с полями - name и surname.
# определяется строковое представление объекта Actor и метаданные модели для отображения у администратора
class Actor(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

# создание модели Genre с  полем name.
# определяется строковое представление объекта Genre и метаданные модели для отображения у администратора
class Genre(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


# создание модели Director с полями - name и surname.
# определяется строковое представление объекта Director и метаданные модели для отображения у администратора
class Director(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'

# создание модели Country с  полем name.
# определяется строковое представление объекта Country и метаданные модели для отображения у администратора
class Country(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

# создание модели Film с полями title, country, year, genre, directors, actors, rating, description, poster, slug
# определяется строковое представление объекта Country и метаданные модели для отображения у администратора
# для genre, directors, country, actors автоматически создаются дополнительные таблицы, которые обеспечивают связи многие ко многим
class Film(models.Model):
    title = models.CharField('Название', max_length=150)
    country = models.ManyToManyField(Country)
    year = models.PositiveSmallIntegerField('Год')
    genre = models.ManyToManyField(Genre)
    directors = models.ManyToManyField(Director)
    actors = models.ManyToManyField(Actor)
    rating = models.FloatField('Рейтинг')
    description = models.TextField('Описание')
    poster = models.URLField('Постер')
    slug = models.SlugField(max_length=150,unique=True, null=True)

    # Метод save переопределен для модели, чтобы автоматически генерировать slug
    # на основе title с помощью функции slugify перед сохранением объекта
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Film, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

