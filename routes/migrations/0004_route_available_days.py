# Generated by Django 4.2.7 on 2024-04-29 18:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_aircraft_airport_alter_city_options_alter_city_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='available_days',
            field=models.DateField(choices=[('MO', 'Понедельник'), ('TU', 'Вторник'), ('WE', 'Среда'), ('TH', 'Четверг'), ('FR', 'Пятница'), ('SA', 'Суббота'), ('SU', 'Воскресенье')], default=django.utils.timezone.now, max_length=2, verbose_name='Дни недели, когда доступен маршрут'),
        ),
    ]
