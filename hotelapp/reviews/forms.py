from datetime import timedelta
import datetime
from typing import Dict, List
from django import forms
from django.forms import fields
from django.utils.translation import check_for_language

from reservations.models import Reservation, Room, RoomReservation, Service, Breakfast
from users.models import CustomUser


class ReviewForm(forms.Form):

    hotel_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    room_no = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    rating = forms.IntegerField(required=True,max_value=10,min_value=1)
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
                rv[j.rr_id] = [j.hotel_id,j.room_no]

        return rv


