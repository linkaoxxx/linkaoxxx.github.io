from django.urls import path
from main import views
from routes.views import routes

app_name ='main'

urlpatterns = [
    path('', views.index, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('shedule/', views.shedule, name='shedule'),
    path('shedule_s/', views.shedule_s, name='shedule_s')
]