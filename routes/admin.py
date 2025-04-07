from django.contrib import admin
from django import forms
from .models import PassengerSeatAssignment, city, airport, aircraft, route, flight, DayOfWeek, seat, cabin
from .models import AdultPassenger, ChildPassenger, Pet, Passenger, Booking

admin.site.register(city)
admin.site.register(airport)
admin.site.register(aircraft)
admin.site.register(flight)
admin.site.register(DayOfWeek)
admin.site.register(seat)
admin.site.register(cabin)

class RouteAdminForm(forms.ModelForm):
    class Meta:
        model = route
        fields = '__all__'
        # widgets = {
        #     'available_days': forms.CheckboxSelectMultiple,
        # }

class RouteAdmin(admin.ModelAdmin):
    form = RouteAdminForm

admin.site.register(route, RouteAdmin)

admin.site.register(AdultPassenger)
admin.site.register(ChildPassenger)
admin.site.register(Pet)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight')  # Отображение колонок в списке
    search_fields = ('user__username', 'flight__name')  # Поля поиска (зависит от ваших полей в моделях User и Flight)
    filter_horizontal = ('passengers', 'seat_assignments')  # Удобное отображение ManyToMany полей

admin.site.register(Booking, BookingAdmin)  # Регистрация модели Booking

class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'document_type', 'passport_series', 'passport_number')
    search_fields = ('name', 'surname', 'passport_number')

class PassengerSeatAssignmentAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'seat')
    search_fields = ('passenger__name', 'seat')

admin.site.register(Passenger)
admin.site.register(PassengerSeatAssignment)