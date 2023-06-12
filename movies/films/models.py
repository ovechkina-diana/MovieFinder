from django.db import models

# Create your models here.

class Films(models.Model):
    title = models.CharField('Название', max_length=50)
    genre = models.CharField('Жанр', max_length=50, default='')
    description = models.TextField('Описание')
    year = models.PositiveSmallIntegerField('Год')

    def get_absolute_url(self):
        return f'/films/{self.id}'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'