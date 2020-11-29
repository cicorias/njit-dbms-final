from datetime import timedelta
import datetime
from typing import Dict, List
from django import forms
from django.forms import fields
from django.utils.translation import check_for_language

from .models import CreditCard, Hotel, Reservation, Room, RoomReservation, Service
from .fields import EmptyChoiceField, EmptyMultipleChoiceField

class ReservationForm(forms.Form):

    hotel = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    check_in = forms.DateField(initial=datetime.date.today, required=True)
    t_check_out = datetime.datetime.now()+timedelta(days=1)
    check_out = forms.DateField(initial=t_check_out, required=True)

    room_choice = forms.ChoiceField(required=True, choices=Room.ROOM_TYPE_CHOICES)

    discount = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    service = EmptyMultipleChoiceField(widget=forms.CheckboxSelectMultiple()) #, initial=get_services())
    breakfast = EmptyChoiceField()
    breakfast_number_orders = forms.IntegerField(required=False, min_value=0, max_value=8) # should be capaicity?

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
    credit_card_year = forms.ChoiceField(required=True, choices=YEAR_CHOICES, initial=("2021", "2021"))
    credit_card_name = forms.CharField(required=True, max_length=20)
    credit_card_type = forms.ChoiceField(required=True, choices=CreditCard.CC_CHOICES)
    credit_card_code = forms.CharField(required=True, max_length=4)
    credit_card_address = forms.CharField(required=True, max_length=40)

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    @staticmethod
    def get_services(hotel: Hotel) -> Dict:
        rv = {}
        #h = Hotel.objects.get(pk=self.initial['hotel'].pk)
        s = hotel.service_set.all()
        for i in s:
            rv[i.sid] = i.s_type

        return [(k, v) for k, v in rv.items()]

    @staticmethod
    def get_breakfast(hotel: Hotel) -> Dict:
        rv = {}
        #h = Hotel.objects.get(pk=self.initial['hotel'].pk)
        s = hotel.breakfast_set.all()
        for i in s:
            rv[i.bid] = i.b_type

        return [(k, v) for k, v in rv.items()]

    @staticmethod
    def get_rooms(hotel: Hotel) -> Dict:
        rv = {}
        s = hotel.room_set.all()
        for i in s:
            rv[i.room_id] = f'{i.room_type} - room number: {i.room_no} - floor: {i.floor}' 

        return [(k, v) for k, v in rv.items()]

    @staticmethod
    def get_discounts(room_key: int, check_in: fields.DateField, check_out: fields.DateField) -> str:
        rv = ''
        room = Room.objects.get(pk = room_key)
        d = room.discountedroom_set.all()
        t = d.filter(start_date__range=(check_in.initial(), check_out.initial.date()))
        for i in t:
            rv += f' {i.discount}'
        return rv


class HotelSelectionForm(forms.Form):
    country = forms.CharField(label = 'country', max_length=20)
    state = forms.CharField(label = 'state',)

    def __init__(self, *args, **kwargs):
        super(HotelSelectionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
