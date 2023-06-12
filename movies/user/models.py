from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Genre, Film

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    films = models.ManyToManyField(Film, through="Enrollment")

class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    film = models.ForeignKey(Film,  on_delete=models.CASCADE)
    isViewed = models.BooleanField(default=False)
