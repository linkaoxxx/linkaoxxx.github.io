# Generated by Django 4.2.7 on 2024-05-31 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0014_adultpassenger_seat_childpassenger_seat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
