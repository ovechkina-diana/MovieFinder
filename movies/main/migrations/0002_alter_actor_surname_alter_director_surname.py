# Generated by Django 4.1.7 on 2023-06-01 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='surname',
            field=models.CharField(max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='director',
            name='surname',
            field=models.CharField(max_length=150, verbose_name='Фамилия'),
        ),
    ]
