from datetime import timedelta
import datetime
from typing import Dict
from django import forms
from django.forms import fields

from .models import Hotel, Reservation, Room, RoomReservation, Service
from .fields import EmptyChoiceField, EmptyMultipleChoiceField

# https://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django/14901714#14901714
# https://github.com/jazzband/django-formtools
# https://django-formtools.readthedocs.io/en/latest/wizard.html
# adding to model admin site https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = RoomReservation
#         fields = ('hotel_id', 'check_in_date', 'check_out_date',)

class ReservationForm(forms.Form):

    hotel = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    check_in = forms.DateField(initial=datetime.date.today, required=True)
    check_out = forms.DateField(initial=datetime.datetime.now()+timedelta(days=1), required=True)

    room_choice = forms.ChoiceField(required=True, choices=Room.ROOM_TYPE_CHOICES)

    service = EmptyMultipleChoiceField(widget=forms.CheckboxSelectMultiple()) #, initial=get_services())
    breakfast = EmptyChoiceField()

    credit_card_number = forms.CharField(required=True, max_length=20)
    # c_card_date = forms.DateField(required=True)

    MONTH_CHOICES = (
        ("1", "Jan"),
        ("2", "Feb"),
        ("3", "Mar"),
        ("4", "Apr"),
        ("5", "May"),
        ("6", "Jun"),
        ("7", "Jul"),
        ("8", "Aug"),
        ("9", "Sep"),
        ("10", "Oct"),
        ("11", "Nov"),
        ("12", "Dec")
    )

    YEAR_CHOICES = (
        ("2020", "2020"),
        ("2021", "2021"),
        ("2022", "2022"),
        ("2023", "2023"),
        ("2024", "2024"),
        ("2025", "2025"),
    )

    credit_card_month = forms.ChoiceField(required=True, choices=MONTH_CHOICES)
    creidt_card_year = forms.ChoiceField(required=True, choices=YEAR_CHOICES)
    credit_card_name = forms.CharField(required=True, max_length=20)

    # def save(self):
    #     pass


    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    @staticmethod
    def get_services(hotel) -> Dict:
        rv = {}
        #h = Hotel.objects.get(pk=self.initial['hotel'].pk)
        s = hotel.service_set.all()
        for i in s:
            rv[i.sid] = i.s_type

        return [(k, v) for k, v in rv.items()]

    @staticmethod
    def get_breakfast(hotel) -> Dict:
        rv = {}
        #h = Hotel.objects.get(pk=self.initial['hotel'].pk)
        s = hotel.breakfast_set.all()
        for i in s:
            rv[i.bid] = i.b_type

        return [(k, v) for k, v in rv.items()]

# class ServiceSelect(forms.Select):
#     def 


class HotelSelectionForm(forms.Form):
    country = forms.CharField(label = 'country', max_length=20)
    state = forms.CharField(label = 'state',)
