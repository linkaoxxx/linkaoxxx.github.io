from django.urls import path
from routes import views

app_name ='routes'

urlpatterns = [
    path('', views.routes, name='index'),
    path('mapB/<int:flight_id>/', views.mapB, name='mapB'),
    path('mapS/<int:flight_id>/', views.mapS, name='mapS'),
    path('mapT/<int:flight_id>/', views.mapT, name='mapT'),
    path('mapA/<int:flight_id>/', views.mapA, name='mapA'),
    path('pas/', views.pas, name='pas'),
    path('save_seats/', views.save_seats, name='save_seats'),
    path('save-adult-passenger/', views.save_adult_passenger, name='save_adult_passenger'),
    path('save-child-passenger/', views.save_child_passenger, name='save_child_passenger'),
    path('save-pet/', views.save_pet, name='save_pet'),
    path('get_user_seat_assignments/', views.get_user_seat_assignments, name='get_user_seat_assignments'),
    path('booking_detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('qr_code/<int:booking_id>/', views.qr_code, name='qr_code'),
    ]
