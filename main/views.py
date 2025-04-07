from django.shortcuts import render
from routes.models import flight, city

def index(request):
    cities = city.objects.all()

    context = {
        'cities': cities
    }
    return render(request, 'main/index.html', context)

def aboutus(request):
    return render(request, 'main/aboutus.html')

def shedule(request):
    return render(request, 'main/shedule.html')

def shedule_s(request):
    return render(request, 'main/shedule_s.html')

