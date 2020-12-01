from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic import View, TemplateView
from reviews.forms import ReviewForm
from typing import Any, Dict, Tuple
from django.forms.fields import CharField
from django import forms
from reservations.models import RoomReview,Hotel,Room,RoomReservation
from django.db import transaction

# Create your views here.

def review_list(request: HttpRequest) -> HttpResponse:
    context = {}
    rv = {}
    resvs = request.user.reservation_set.all()
    for i in resvs:
        for j in i.roomreservation_set.all():
            rv[j.rr_id] = f'date: {i.r_date} - {j.hotel_id} - checkin: {j.check_in_date} through {j.check_out_date}'

    context['reservations'] = rv #  [(k, v) for k, v in rv.items()]
    return render(request, 'review_list.html', context)



def add_reviews(request: HttpRequest, id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        room_no = RoomReservation.objects.get(rr_id=id).room_no_id
        room = get_object_or_404(Room,room_no= room_no)
        

        if form.is_valid():

            roomreview = RoomReview()
            roomreview.room_id = room
            roomreview.rating = form.data['rating']
            roomreview.text_content = form.data['text']
            roomreview.cid = request.user
            roomreview.save()

            return redirect("reviews")

    else :
        initial = {}
        context = {}
        user = request.user
        initial['user'] = user
        form = ReviewForm(initial=initial)

        room_reservations = form.get_room_reservations(user)

        for i in room_reservations:
            values = room_reservations.get(i)
            
            form.fields['hotel_id'] = CharField(initial=values[0], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            form.fields['room_no'] = CharField(initial=values[1], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        context['form'] = form
        

    return render(request, 'add_reviews.html', context)