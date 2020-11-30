from datetime import timedelta
import datetime
from typing import Dict, List
from django import forms
from django.forms import fields
from django.utils.translation import check_for_language

from reservations.models import Reservation, Room, RoomReservation, Service, Breakfast
from users.models import CustomUser
from reservations.fields import EmptyChoiceField, EmptyMultipleChoiceField

class ReviewForm(forms.Form):

    hotel = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    RATING_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10")
    )
    rating = forms.ChoiceField(required=True, choices=RATING_CHOICES)
    text = forms.CharField(max_length=40)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

    @staticmethod
    def get_room_reservations(user: CustomUser) -> Dict:
        rv = {}
        resvs = user.reservation_set.all()
        for i in resvs:
            for j in i.roomreservation_set.all():
                rv[i.invoice_number] = f'hotel id:{j.hotel_id}'
                rv[i.invoice_number].append(f'room number:{j.room_no}')

        return [(k, v) for k, v in rv.items()]


