from django.contrib import admin
from .models import Actor, Genre, Director, Film

# Добаленные модели в панель администратора

admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Director)
admin.site.register(Film)