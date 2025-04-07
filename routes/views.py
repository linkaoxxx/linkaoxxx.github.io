from io import BytesIO
from lib2to3.fixes.fix_input import context
from django.shortcuts import render, redirect, get_object_or_404
import qrcode
from .models import cabin, flight, city, seat, AdultPassenger, ChildPassenger, Pet, PassengerSeatAssignment, Passenger, Booking
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.datetime_safe import datetime
from django.http import JsonResponse
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.core.files.base import ContentFile

def routes(request):
    # Получаем параметры из запроса GET
    from_city_name = request.GET.get('from')
    to_city_name = request.GET.get('to')
    date_str = request.GET.get('date')

    # Преобразуем дату в формат YYYY-MM-DD
    date = None
    if date_str:
        try:
            date = datetime.strptime(date_str, '%d.%m.%Y').strftime('%Y-%m-%d')
        except ValueError:
            # Обработка ошибки в случае неверного формата даты
            pass

    # Получаем объекты рейсов
    flight_routes = flight.objects.all()

    # Фильтруем рейсы по городам и дате
    if from_city_name:
        flight_routes = flight_routes.filter(route__departure_airport__city__name=from_city_name)
    if to_city_name:
        flight_routes = flight_routes.filter(route__destination_airport__city__name=to_city_name)
    if date:
        flight_routes = flight_routes.filter(departure_date__date=date)

    # Получаем список всех городов для отображения в выпадающих списках
    cities = city.objects.all()

    # Определение базовой цены для взрослого билета
    base_adult_price = 0
    for fl in flight_routes:
        base_adult_price = fl.route.price
        break

     # Получение количества пассажиров каждой категории из запроса GET
    adult_count_raw = request.GET.get('adult')
    adult_count = int(adult_count_raw) if adult_count_raw else 1

    child_count_raw = request.GET.get('child')
    child_count = int(child_count_raw) if child_count_raw else 0

    pet_count_raw = request.GET.get('pet')
    pet_count = int(pet_count_raw) if pet_count_raw else 0

    # Рассчитываем цены для различных категорий пассажиров
    adult_price = base_adult_price

    # Подсчет общего количества пассажиров
    total_passengers = adult_count + child_count + pet_count

    # Рассчитываем цены для различных категорий пассажиров
    adult_price = base_adult_price
    child_price = Decimal('0.75') * base_adult_price  # 75% от стоимости взрослого билета
    pet_price = Decimal('0.5') * base_adult_price  # 50% от стоимости взрослого билета

    # Проверка наличия числовых значений и установка минимального значения равного 1 для взрослых
    adult_count = max(adult_count, 1)

    # Подсчет общей стоимости билетов
    total_price = (base_adult_price * adult_count) + (child_price * child_count) + (pet_price * pet_count)

    context = {
       'title': 'NEBO - Рейсы',
        'routes': flight_routes,
        'from_city': from_city_name,
        'to_city': to_city_name,
        'date': date_str,
        'cities': cities,  # добавляем список городов в контекст
        'total_price': total_price,  # добавляем общую цену в контекст
        'adult_price': adult_price,
        'child_price': child_price,
        'pet_price': pet_price,
        'total_passengers': total_passengers,  # добавляем общее количество пассажиров в контекст
        'adult_count': adult_count,
        'child_count': child_count,
        'pet_count': pet_count,
    }

    return render(request, 'routes/routes.html', context)



# def flight_list(request):
#     return HttpResponse("Flight list view")
    
def mapB(request, flight_id):
    print("Received request for flight ID:", flight_id)
    flight_instance = get_object_or_404(flight, id=flight_id)
    boeing_cabins = cabin.objects.filter(aircraft__model_name='Boeing 737-800NG') 
    taken_seats = {seat.seat_number: seat.is_taken for cabin in boeing_cabins for seat in cabin.seats.all()}

    adult_count_raw = request.GET.get('adult')
    adult_count = int(adult_count_raw) if adult_count_raw else 0

    child_count_raw = request.GET.get('child')
    child_count = int(child_count_raw) if child_count_raw else 0

    pet_count_raw = request.GET.get('pet')
    pet_count = int(pet_count_raw) if pet_count_raw else 0

    adult_forms = [{'type': 'adult'} for _ in range(adult_count)]
    child_forms = [{'type': 'child'} for _ in range(child_count)]
    pet_forms = [{'type': 'pet'} for _ in range(pet_count)]

    flight_routes = flight.objects.filter(id=flight_id)
    base_adult_price = flight_routes.first().route.price if flight_routes.exists() else 0
    for fl in flight_routes:
        base_adult_price = fl.route.price
        break

    adult_price = base_adult_price
    child_price = Decimal('0.75') * base_adult_price
    pet_price = Decimal('0.5') * base_adult_price

    adult_count = max(adult_count, 1)

    total_price = (base_adult_price * adult_count) + (child_price * child_count) + (pet_price * pet_count)

    print("Base adult price:", base_adult_price)
    print("Total price:", total_price)
    print("Adult count:", adult_count)
    print("Child count:", child_count)
    print("Pet count:", pet_count)

    context = {
        'flight_instance': flight_instance,
        'cabins': boeing_cabins,
        'taken_seats_json': taken_seats,
        'adult_forms': adult_forms,
        'child_forms': child_forms,
        'pet_forms': pet_forms,
        'total_price': total_price,
    }
    return render(request, 'routes/mapB.html', context)

def mapS(request, flight_id):
    print("Received request for flight ID:", flight_id)
    flight_instance = get_object_or_404(flight, id=flight_id)
    sukhoi_cabins = cabin.objects.filter(aircraft__model_name='Sukhoi Superjet 100') 
    taken_seats = {seat.seat_number: seat.is_taken for cabin in sukhoi_cabins for seat in cabin.seats.all()}

    adult_count_raw = request.GET.get('adult')
    adult_count = int(adult_count_raw) if adult_count_raw else 0

    child_count_raw = request.GET.get('child')
    child_count = int(child_count_raw) if child_count_raw else 0

    pet_count_raw = request.GET.get('pet')
    pet_count = int(pet_count_raw) if pet_count_raw else 0

    adult_forms = [{'type': 'adult'} for _ in range(adult_count)]
    child_forms = [{'type': 'child'} for _ in range(child_count)]
    pet_forms = [{'type': 'pet'} for _ in range(pet_count)]

    flight_routes = flight.objects.filter(id=flight_id)
    base_adult_price = flight_routes.first().route.price if flight_routes.exists() else 0
    for fl in flight_routes:
        base_adult_price = fl.route.price
        break

    adult_price = base_adult_price
    child_price = Decimal('0.75') * base_adult_price
    pet_price = Decimal('0.5') * base_adult_price

    adult_count = max(adult_count, 1)

    total_price = (base_adult_price * adult_count) + (child_price * child_count) + (pet_price * pet_count)

    print("Base adult price:", base_adult_price)
    print("Total price:", total_price)
    print("Adult count:", adult_count)
    print("Child count:", child_count)
    print("Pet count:", pet_count)

    context = {
        'flight_instance': flight_instance,
        'cabins': sukhoi_cabins,
        'taken_seats_json': taken_seats,
        'adult_forms': adult_forms,
        'child_forms': child_forms,
        'pet_forms': pet_forms,
        'total_price': total_price,
    }
    return render(request, 'routes/mapS.html', context)

def mapT(request, flight_id):
    print("Received request for flight ID:", flight_id)
    flight_instance = get_object_or_404(flight, id=flight_id)
    tu_cabins = cabin.objects.filter(aircraft__model_name='TU 204') 
    taken_seats = {seat.seat_number: seat.is_taken for cabin in tu_cabins for seat in cabin.seats.all()}

    adult_count_raw = request.GET.get('adult')
    adult_count = int(adult_count_raw) if adult_count_raw else 0

    child_count_raw = request.GET.get('child')
    child_count = int(child_count_raw) if child_count_raw else 0

    pet_count_raw = request.GET.get('pet')
    pet_count = int(pet_count_raw) if pet_count_raw else 0

    adult_forms = [{'type': 'adult'} for _ in range(adult_count)]
    child_forms = [{'type': 'child'} for _ in range(child_count)]
    pet_forms = [{'type': 'pet'} for _ in range(pet_count)]

    flight_routes = flight.objects.filter(id=flight_id)
    base_adult_price = flight_routes.first().route.price if flight_routes.exists() else 0
    for fl in flight_routes:
        base_adult_price = fl.route.price
        break

    adult_price = base_adult_price
    child_price = Decimal('0.75') * base_adult_price
    pet_price = Decimal('0.5') * base_adult_price

    adult_count = max(adult_count, 1)

    total_price = (base_adult_price * adult_count) + (child_price * child_count) + (pet_price * pet_count)

    print("Base adult price:", base_adult_price)
    print("Total price:", total_price)
    print("Adult count:", adult_count)
    print("Child count:", child_count)
    print("Pet count:", pet_count)

    context = {
        'flight_instance': flight_instance,
        'cabins': tu_cabins,
        'taken_seats_json': taken_seats,
        'adult_forms': adult_forms,
        'child_forms': child_forms,
        'pet_forms': pet_forms,
        'total_price': total_price,
    }
    return render(request, 'routes/mapT.html', context)

def mapA(request, flight_id):
    print("Received request for flight ID:", flight_id)
    flight_instance = get_object_or_404(flight, id=flight_id)
    airbus_cabins = cabin.objects.filter(aircraft__model_name='Airbus A350-900') 
    taken_seats = {seat.seat_number: seat.is_taken for cabin in airbus_cabins for seat in cabin.seats.all()}

    adult_count_raw = request.GET.get('adult')
    adult_count = int(adult_count_raw) if adult_count_raw else 0

    child_count_raw = request.GET.get('child')
    child_count = int(child_count_raw) if child_count_raw else 0

    pet_count_raw = request.GET.get('pet')
    pet_count = int(pet_count_raw) if pet_count_raw else 0

    adult_forms = [{'type': 'adult'} for _ in range(adult_count)]
    child_forms = [{'type': 'child'} for _ in range(child_count)]
    pet_forms = [{'type': 'pet'} for _ in range(pet_count)]

    flight_routes = flight.objects.filter(id=flight_id)
    base_adult_price = flight_routes.first().route.price if flight_routes.exists() else 0
    for fl in flight_routes:
        base_adult_price = fl.route.price
        break

    adult_price = base_adult_price
    child_price = Decimal('0.75') * base_adult_price
    pet_price = Decimal('0.5') * base_adult_price

    adult_count = max(adult_count, 1)

    total_price = (base_adult_price * adult_count) + (child_price * child_count) + (pet_price * pet_count)

    print("Base adult price:", base_adult_price)
    print("Total price:", total_price)
    print("Adult count:", adult_count)
    print("Child count:", child_count)
    print("Pet count:", pet_count)

    context = {
        'flight_instance': flight_instance,
        'cabins': airbus_cabins,
        'taken_seats_json': taken_seats,
        'adult_forms': adult_forms,
        'child_forms': child_forms,
        'pet_forms': pet_forms,
        'total_price': total_price,
    }
    return render(request, 'routes/mapA.html', context)

@csrf_exempt
def save_seats(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        flight_id = data.get('flight_id')
        selected_seats = data.get('selected_seats')
        user = request.user
        
        flight_instance = get_object_or_404(flight, id=flight_id)
        
        for seat_info in selected_seats:
            seat_instance = get_object_or_404(seat, id=seat_info['seat_id'])
            row_instance = cabin.get_row_instance(aircraft=flight_instance.aircraft, row_number=seat_info['row_number'])
            PassengerSeatAssignment.objects.create(
                user=user,
                seat=seat_instance,
                flight=flight_instance,
                row=row_instance
            )
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed'}, status=400)

def pas(request):
    # Получаем URL из запроса
    url = request.build_absolute_uri()
    
    # Проверяем наличие параметров adult, child и pet в URL и считаем количество пассажиров
    adult_count = url.count('adult=')
    child_count = url.count('child=')
    pet_count = url.count('pet=')
    
    # Вычисляем общее количество пассажиров
    total_passengers = adult_count + child_count + pet_count
    
    # Возвращаем количество пассажиров в виде JSON-ответа
    return render(request, 'routes/pas.html', {'total_passengers': total_passengers})

def save_adult_passenger(request):
    if request.method == 'POST':
        try:
            adult_passenger = AdultPassenger(
                name=request.POST.get('name'),
                surname=request.POST.get('surname'),
                patronymic=request.POST.get('patronymic'),
                document_type=request.POST.get('document_type'),
                passport_series=request.POST.get('passport_series'),
                passport_number=request.POST.get('passport_number'),
                foreign_passport_series=request.POST.get('foreign_passport_series'),
                foreign_passport_number=request.POST.get('foreign_passport_number'),
                has_luggage_10kg=request.POST.get('has_luggage_10kg') == 'on',
                has_luggage_20kg=request.POST.get('has_luggage_20kg') == 'on',
                seat_id=request.POST.get('seat')  # Используем seat_id для сохранения места
            )
            adult_passenger.save()

            Passenger.objects.create(
                content_object=adult_passenger,
                passenger_type='adult',
                name=adult_passenger.name,
                surname=adult_passenger.surname,
                document_type=adult_passenger.document_type,
                passport_series=adult_passenger.passport_series,
                passport_number=adult_passenger.passport_number,
                foreign_passport_series=adult_passenger.foreign_passport_series,
                foreign_passport_number=adult_passenger.foreign_passport_number,
                has_luggage_10kg=adult_passenger.has_luggage_10kg,
                has_luggage_20kg=adult_passenger.has_luggage_20kg,
                seat_id=adult_passenger.seat_id
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return HttpResponseBadRequest('Invalid request')

def save_child_passenger(request):
    if request.method == 'POST':
        try:
            child_passenger = ChildPassenger(
                name=request.POST.get('name'),
                surname=request.POST.get('surname'),
                patronymic=request.POST.get('patronymic'),
                document_type=request.POST.get('document_type'),
                passport_series=request.POST.get('passport_series'),
                passport_number=request.POST.get('passport_number'),
                birth_certificate_series=request.POST.get('birth_certificate_series'),
                birth_certificate_number=request.POST.get('birth_certificate_number'),
                foreign_passport_series=request.POST.get('foreign_passport_series'),
                foreign_passport_number=request.POST.get('foreign_passport_number'),
                has_luggage_10kg=request.POST.get('has_luggage_10kg') == 'on',
                has_luggage_20kg=request.POST.get('has_luggage_20kg') == 'on',
                seat_id=request.POST.get('seat')  # Используем seat_id для сохранения места
            )
            child_passenger.save()

            Passenger.objects.create(
                content_object=child_passenger,
                passenger_type='child',
                name=child_passenger.name,
                surname=child_passenger.surname,
                document_type=child_passenger.document_type,
                passport_series=child_passenger.passport_series,
                passport_number=child_passenger.passport_number,
                foreign_passport_series=child_passenger.foreign_passport_series,
                foreign_passport_number=child_passenger.foreign_passport_number,
                has_luggage_10kg=child_passenger.has_luggage_10kg,
                has_luggage_20kg=child_passenger.has_luggage_20kg,
                birth_certificate_series=child_passenger.birth_certificate_series,
                birth_certificate_number=child_passenger.birth_certificate_number,
                seat_id=child_passenger.seat_id
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return HttpResponseBadRequest('Invalid request')

def save_pet(request):
    if request.method == 'POST':
        try:
            pet = Pet(
                species=request.POST.get('species'),
                name=request.POST.get('name'),
                breed=request.POST.get('breed'),
                vet_passport_number=request.POST.get('vet_passport_number'),
                vaccination_certificate_number=request.POST.get('vaccination_certificate_number'),
                seat_id=request.POST.get('seat')  # Используем seat_id для сохранения места
            )
            pet.save()

            Passenger.objects.create(
                content_object=pet,
                passenger_type='pet',
                name=pet.name,
                breed=pet.breed,
                vet_passport_number=pet.vet_passport_number,
                vaccination_certificate_number=pet.vaccination_certificate_number,
                seat_id=pet.seat_id
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return HttpResponseBadRequest('Invalid request')
    
@require_GET
def get_user_seat_assignments(request):
    
    limit = int(request.GET.get('limit', 3))  # Получаем значение параметра limit из URL, по умолчанию 10
    assignments = PassengerSeatAssignment.objects.all().order_by('-id')[:limit]
    
    # Формируем список мест для JSON-ответа
    seats = [{'row': assignment.row.id, 'seat': assignment.seat.id} for assignment in assignments]
    
    # Возвращаем JSON-ответ с местами
    return JsonResponse({'seats': seats})

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    route_price = booking.flight.route.price
    total_price = route_price * booking.passengers.count()
    luggage_price = 0
    for passenger in booking.passengers.all():
        if passenger.has_luggage_10kg:
            luggage_price += 500
        if passenger.has_luggage_20kg:
            luggage_price += 1500  
    total_price += luggage_price

    total_amount_in_cents = int(total_price * 100)

    qr_data = (
        f"ST00012|Name=АВИАКОМПАНИЯНЕБО|PersonalAcc=40817810711524044721|"
        f"BankName=ВТБ|BIC=043601968|CorrespAcc=30101810422023601968|"
        f"Currency=RUB|Sum={total_amount_in_cents}|Purpose=Оплата заказа №{booking.id}"
    )

    buffer = BytesIO()
    qr = qrcode.make(qr_data)
    qr.save(buffer, format="PNG")

    qr_image_file = ContentFile(buffer.getvalue(), 'qr_code.png')  # Создание файла
    booking.qr_image.save('qr_code.png', qr_image_file, save=True)

    return render(request, 'routes/booking_detail.html', {
        'booking': booking,
        'total_price': total_price,
        'luggage_price': luggage_price,
        'route_price': route_price
    })

@require_POST
def create_booking(request):
    data = json.loads(request.body)
    user = request.user
    flight_id = data.get('flight_id')
    passenger_ids = data.get('passenger_ids')
    seat_assignment_ids = data.get('seat_assignment_ids')

    flight = get_object_or_404(flight, id=flight_id)
    passengers = Passenger.objects.filter(id__in=passenger_ids)
    seat_assignments = PassengerSeatAssignment.objects.filter(id__in=seat_assignment_ids)

    booking = Booking.objects.create(user=user, flight=flight)
    booking.passengers.set(passengers)
    booking.seat_assignments.set(seat_assignments)
    booking.save()

    return JsonResponse({'status': 'success', 'booking_id': booking.id})

def qr_code(request, booking_id):
    booking = Booking.objects.get(pk=booking_id)  # Получение заказа по ID
    qr_image_url = booking.qr_image.url if booking.qr_image else None  # URL изображения QR-кода

    context = {
        'qr_image_url': qr_image_url,  # Передача URL изображения в контекст
    }

    return render(request, 'routes/qr_code.html', context)

