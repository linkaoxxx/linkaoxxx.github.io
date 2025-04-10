# Generated by Django 4.2.7 on 2024-05-03 10:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_alter_dayofweek_options_alter_dayofweek_table_seat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='arrival_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата прилета'),
        ),
        migrations.AddField(
            model_name='flight',
            name='flight_duration',
            field=models.CharField(default=1, max_length=100, verbose_name='Время в полете'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flight',
            name='salon_map_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на карту салона'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='departure_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата вылета'),
        ),
    ]
