from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings

# from .models import flight

class city(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    
    class Meta:
        db_table = 'city'
        verbose_name = 'город'
        verbose_name_plural = 'города'
    
    def __str__(self):
        return self.name

class airport(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название аэропорта')
    city = models.ForeignKey(city, on_delete=models.CASCADE, related_name='airports', verbose_name='Город')

    class Meta:
        db_table = 'airport'
        verbose_name = 'аэропорт'
        verbose_name_plural = 'аэропорты'
    
    def __str__(self):
        return self.name


class aircraft(models.Model):
    model_name = models.CharField(max_length=150, verbose_name='Название модели')
    image = models.ImageField(upload_to='aircraft_images/', verbose_name='Изображение')

    class Meta:
        db_table = 'aircraft'
        verbose_name = 'самолет'
        verbose_name_plural = 'самолеты'
    
    def __str__(self):
        return self.model_name
    
class seat(models.Model):
    aircraft = models.ForeignKey(aircraft, on_delete=models.CASCADE, related_name='seats', verbose_name='Самолет')
    seat_number = models.CharField(max_length=10, verbose_name='Номер места')
    is_taken = models.BooleanField(default=False, verbose_name='Занято ли место')

    class Meta:
        unique_together = ['aircraft', 'seat_number']  # Уникальное место на каждом самолете
        db_table = 'seat'
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return f'{self.seat_number} на {self.aircraft}'

class cabin(models.Model):
    aircraft = models.ForeignKey(aircraft, on_delete=models.CASCADE, related_name='rows', verbose_name='Самолет')
    row_number = models.PositiveIntegerField(verbose_name='Номер ряда')
    seats = models.ManyToManyField(seat, related_name='rows', verbose_name='Места в ряду')

    class Meta:
        unique_together = ['aircraft', 'row_number']  # Уникальный ряд на каждом самолете
        db_table = 'cabin'
        verbose_name = 'ряд'
        verbose_name_plural = 'ряды'

    def __str__(self):
        return f'Ряд {self.row_number} на {self.aircraft}'
    @classmethod
    def get_row_instance(cls, aircraft, row_number):
        try:
            return cls.objects.get(aircraft=aircraft, row_number=row_number)
        except cls.DoesNotExist:
            return None

class DayOfWeek(models.Model):
    name = models.CharField(max_length=15, verbose_name='День недели')

    class Meta:
        db_table = 'dayofweek'
        verbose_name = 'день недели'
        verbose_name_plural = 'дни недели'

    def __str__(self):
        return self.name

class route(models.Model):
    departure_airport = models.ForeignKey(airport, on_delete=models.CASCADE, related_name='departure_routes', verbose_name='Аэропорт вылета')
    destination_airport = models.ForeignKey(airport, on_delete=models.CASCADE, related_name='destination_routes', verbose_name='Аэропорт назначения')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена маршрута')
    available_days = models.ManyToManyField(DayOfWeek, verbose_name='Дни недели, когда доступен маршрут')

    def __str__(self):
        return f'Маршрут от {self.departure_airport} до {self.destination_airport}, Цена: {self.price}'

    class Meta:
        db_table = 'route'
        verbose_name = 'маршрут'
        verbose_name_plural = 'маршруты'

class flight(models.Model):
    route = models.ForeignKey(route, on_delete=models.CASCADE, verbose_name='Маршрут')
    aircraft = models.ForeignKey(aircraft, on_delete=models.CASCADE, verbose_name='Самолет')
    departure_date = models.DateTimeField(default=timezone.now, verbose_name='Дата вылета')
    flight_duration = models.CharField(max_length=100, verbose_name='Время в полете')
    arrival_date = models.DateTimeField(default=timezone.now, verbose_name='Дата прилета')
    salon_map_url = models.URLField(verbose_name='Ссылка на карту салона', blank=True, null=True)
    cabin = models.ForeignKey('Cabin', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Схема салона')

    class Meta:
        db_table = 'flight'
        verbose_name = 'рейс'
        verbose_name_plural = 'рейсы'
    
    def __str__(self):
        return f'{self.route} совершаемый {self.departure_date}'

class Passenger(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    passenger_type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True, null=True)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=50, blank=True, null=True)
    passport_series = models.CharField(max_length=6, blank=True, null=True)
    passport_number = models.CharField(max_length=4, blank=True, null=True)
    foreign_passport_series = models.CharField(max_length=2, blank=True, null=True)
    foreign_passport_number = models.CharField(max_length=7, blank=True, null=True)
    has_luggage_10kg = models.BooleanField(default=False, verbose_name='Багаж до 10 кг')
    has_luggage_20kg = models.BooleanField(default=False, verbose_name='Багаж до 20 кг')
    birth_certificate_series = models.CharField(max_length=3, blank=True, null=True)
    birth_certificate_number = models.CharField(max_length=6, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100, blank=True, null=True)
    vet_passport_number = models.CharField(max_length=100, blank=True, null=True)
    vaccination_certificate_number = models.CharField(max_length=100, blank=True, null=True)
    seat = models.CharField(max_length=10, blank=True, null=True) 
    
class AdultPassenger(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=50)
    passport_series = models.CharField(max_length=6, blank=True, null=True)
    passport_number = models.CharField(max_length=4, blank=True, null=True)
    foreign_passport_series = models.CharField(max_length=2, blank=True, null=True)
    foreign_passport_number = models.CharField(max_length=7, blank=True, null=True)
    has_luggage_10kg = models.BooleanField(default=False, verbose_name='Багаж до 10 кг')
    has_luggage_20kg = models.BooleanField(default=False, verbose_name='Багаж до 20 кг')
    seat = models.CharField(max_length=10, blank=True, null=True) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Passenger.objects.create(
            content_object=self,
            passenger_type='adult',
            name=self.name,
            surname=self.surname,
            patronymic=self.patronymic,
            document_type=self.document_type,
            passport_series=self.passport_series,
            passport_number=self.passport_number,
            foreign_passport_series=self.foreign_passport_series,
            foreign_passport_number=self.foreign_passport_number,
            has_luggage_10kg=self.has_luggage_10kg,
            has_luggage_20kg=self.has_luggage_20kg
        )

class ChildPassenger(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=50)
    passport_series = models.CharField(max_length=6, blank=True, null=True)
    passport_number = models.CharField(max_length=4, blank=True, null=True)
    birth_certificate_series = models.CharField(max_length=3, blank=True, null=True)
    birth_certificate_number = models.CharField(max_length=6, blank=True, null=True)
    foreign_passport_series = models.CharField(max_length=2, blank=True, null=True)
    foreign_passport_number = models.CharField(max_length=7, blank=True, null=True)
    has_luggage_10kg = models.BooleanField(default=False, verbose_name='Багаж до 10 кг')
    has_luggage_20kg = models.BooleanField(default=False, verbose_name='Багаж до 20 кг')
    seat = models.CharField(max_length=10, blank=True, null=True) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Passenger.objects.create(
            content_object=self,
            passenger_type='child',
            name=self.name,
            surname=self.surname,
            document_type=self.document_type,
            passport_series=self.passport_series,
            passport_number=self.passport_number,
            foreign_passport_series=self.foreign_passport_series,
            foreign_passport_number=self.foreign_passport_number,
            has_luggage_10kg=self.has_luggage_10kg,
            has_luggage_20kg=self.has_luggage_20kg,
            birth_certificate_series=self.birth_certificate_series,
            birth_certificate_number=self.birth_certificate_number
        )

class Pet(models.Model):
    species = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    vet_passport_number = models.CharField(max_length=100)
    vaccination_certificate_number = models.CharField(max_length=100)
    seat = models.CharField(max_length=10, blank=True, null=True) 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Passenger.objects.create(
            content_object=self,
            passenger_type='pet',
            name=self.name,
            surname='',
            document_type='',
            passport_series='',
            passport_number=self.vet_passport_number,
            foreign_passport_series='',
            foreign_passport_number=self.vaccination_certificate_number,
            has_luggage_10kg=False,
            has_luggage_20kg=False
        )

class PassengerSeatAssignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    seat = models.ForeignKey('seat', on_delete=models.CASCADE, verbose_name='Место')
    flight = models.ForeignKey('flight', on_delete=models.CASCADE, verbose_name='Рейс')
    row = models.ForeignKey('cabin', on_delete=models.CASCADE, verbose_name='Ряд')
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE, verbose_name='Пассажир')

    class Meta:
        db_table = 'passenger_seat_assignment'
        verbose_name = 'назначение места пользователю'
        verbose_name_plural = 'назначения мест пользователям'

    def __str__(self):
        return f'{self.user} на месте {self.seat} в ряду {self.row} на рейсе {self.flight}'
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    flight = models.ForeignKey(flight, on_delete=models.CASCADE, verbose_name='Рейс')
    passengers = models.ManyToManyField(Passenger, verbose_name='Пассажиры')
    seat_assignments = models.ManyToManyField(PassengerSeatAssignment, verbose_name='Назначенные места')
    qr_image = models.ImageField(upload_to='qr_codes/', null=True, blank=True, verbose_name="QR-код")  # Новое поле для QR-кода

    class Meta:
        db_table = 'booking'
        verbose_name = 'букинг'
        verbose_name_plural = 'букинги'

    def __str__(self):
        return f'Букинг пользователя {self.user} на рейс {self.flight}'