# Generated by Django 4.1.7 on 2023-06-02 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_country_remove_film_country_film_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]