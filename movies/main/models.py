from django.db import models
from slugify import slugify
from django.urls import reverse



class Actor(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

class Genre(models.Model):
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Director(models.Model):
    name = models.CharField('Имя', max_length=100)
    surname = models.CharField('Фамилия', max_length=150)

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'

class Country(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Film, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

