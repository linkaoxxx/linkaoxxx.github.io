# Generated by Django 4.2.7 on 2024-05-24 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('routes', '0008_flight_cabin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdultPassenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('patronymic', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(max_length=50)),
                ('passport_series', models.CharField(blank=True, max_length=6, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=4, null=True)),
                ('foreign_passport_series', models.CharField(blank=True, max_length=2, null=True)),
                ('foreign_passport_number', models.CharField(blank=True, max_length=7, null=True)),
                ('has_luggage_10kg', models.BooleanField(default=False, verbose_name='Багаж до 10 кг')),
                ('has_luggage_20kg', models.BooleanField(default=False, verbose_name='Багаж до 20 кг')),
            ],
        ),
        migrations.CreateModel(
            name='ChildPassenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('patronymic', models.CharField(blank=True, max_length=100, null=True)),
                ('document_type', models.CharField(max_length=50)),
                ('passport_series', models.CharField(blank=True, max_length=6, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=4, null=True)),
                ('birth_certificate_series', models.CharField(blank=True, max_length=3, null=True)),
                ('birth_certificate_number', models.CharField(blank=True, max_length=6, null=True)),
                ('foreign_passport_series', models.CharField(blank=True, max_length=2, null=True)),
                ('foreign_passport_number', models.CharField(blank=True, max_length=7, null=True)),
                ('has_luggage_10kg', models.BooleanField(default=False, verbose_name='Багаж до 10 кг')),
                ('has_luggage_20kg', models.BooleanField(default=False, verbose_name='Багаж до 20 кг')),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('species', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('breed', models.CharField(max_length=100)),
                ('vet_passport_number', models.CharField(max_length=100)),
                ('vaccination_certificate_number', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('passenger_type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('document_type', models.CharField(blank=True, max_length=50, null=True)),
                ('passport_series', models.CharField(blank=True, max_length=6, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=4, null=True)),
                ('foreign_passport_series', models.CharField(blank=True, max_length=2, null=True)),
                ('foreign_passport_number', models.CharField(blank=True, max_length=7, null=True)),
                ('has_luggage_10kg', models.BooleanField(default=False, verbose_name='Багаж до 10 кг')),
                ('has_luggage_20kg', models.BooleanField(default=False, verbose_name='Багаж до 20 кг')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
    ]
