# Generated by Django 4.1.7 on 2023-06-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_enrollment_userprofile_films'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='isViewed',
            field=models.BooleanField(default=False),
        ),
    ]
