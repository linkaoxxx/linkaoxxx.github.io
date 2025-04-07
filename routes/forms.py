from django import forms
from .models import AdultPassenger, ChildPassenger, Pet

class AdultPassengerForm(forms.ModelForm):
    document_type = forms.ChoiceField(
        choices=(
            ('passport', 'Паспорт'),
            ('foreign_passport', 'Загранпаспорт'),
        ),
        label='Тип документа',
    )
    
    name = forms.CharField(label='Имя')
    surname = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')

    class Meta:
        model = AdultPassenger
        fields = ['name', 'surname', 'patronymic', 'document_type', 'passport_series', 'passport_number', 'foreign_passport_series', 'foreign_passport_number', 'has_luggage_10kg', 'has_luggage_20kg']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'passport_series': 'Серия паспорта',
            'passport_number': 'Номер паспорта',
            'foreign_passport_series': 'Серия заграничного паспорта',
            'foreign_passport_number': 'Номер заграничного паспорта',
            'has_luggage_10kg': 'Багаж до 10 кг',
            'has_luggage_20kg': 'Багаж до 20 кг',
        }


class ChildPassengerForm(forms.ModelForm):
    document_type = forms.ChoiceField(
        choices=(
            ('passport', 'Паспорт'),
            ('foreign_passport', 'Заграничный паспорт'),
            ('birth_certificate', 'Свидетельство о рождении'),  # Добавлено свидетельство о рождении
        ),
        label='Тип документа',
    )

    name = forms.CharField(label='Имя')
    surname = forms.CharField(label='Фамилия')
    patronymic = forms.CharField(label='Отчество')


    class Meta:
        model = ChildPassenger
        fields = ['name', 'surname', 'patronymic', 'document_type', 'passport_series', 'passport_number', 'birth_certificate_series', 'birth_certificate_number', 'foreign_passport_series', 'foreign_passport_number', 'has_luggage_10kg', 'has_luggage_20kg']
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronymic': 'Отчество',
            'passport_series': 'Серия паспорта',
            'passport_number': 'Номер паспорта',
            'birth_certificate_series': 'Серия свидетельства о рождении',
            'birth_certificate_number': 'Номер свидетельства о рождении',
            'foreign_passport_series': 'Серия заграничного паспорта',
            'foreign_passport_number': 'Номер заграничного паспорта',
            'has_luggage_10kg': 'Багаж до 10 кг',
            'has_luggage_20kg': 'Багаж до 20 кг',
        }



class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['species', 'name', 'breed', 'vet_passport_number', 'vaccination_certificate_number']
        labels = {
            'species': 'Вид',
            'name': 'Имя',
            'breed': 'Порода',
            'vet_passport_number': 'Номер ветеринарного паспорта',
            'vaccination_certificate_number': 'Номер сертификата о вакцинации',
        }
