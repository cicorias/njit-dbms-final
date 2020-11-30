from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.views.generic import View, TemplateView
from reviews.forms import ReviewForm
from typing import Any, Dict, Tuple
from django.forms.fields import ChoiceField

# Create your views here.

def review_list(request: HttpRequest) -> HttpResponse:
    context = {}
    rv = {}
    resvs = request.user.reservation_set.all()
    for i in resvs:
        for j in i.roomreservation_set.all():
            rv[j] = f'date: {i.r_date} - {j.hotel_id} - checkin: {j.check_in_date} through {j.check_out_date}'

    context['reservations'] = rv #  [(k, v) for k, v in rv.items()]
    return render(request, 'review_list.html', context)


def add_reviews(request: HttpRequest)-> HttpResponse:
    if request.method == "GET":
        initial = {}
        context = {}
        user = request.user
        initial['user'] = user
        form = ReviewForm(initial=initial)

        room_reservations = form.get_room_reservations(user).values()
        for v in room_reservations:
            val = room_reservations[v]
            form.fields[val] = ChoiceField(required=True, choices=val)
            

        form.get_room_number

        context['form'] = form

    return render(request, 'add_reviews.html', context)