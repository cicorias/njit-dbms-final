from typing import Any, Dict, Tuple
from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxInput
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.views.generic import View, TemplateView
from django import forms
from datetime import timedelta
import datetime
import uuid
from reservations.fields import EmptyChoiceField, EmptyMultipleChoiceField

from users.models import CustomUser
from .forms import HotelSelectionForm, ReservationForm

from .models import Hotel, Service

### https://simpleit.rocks/python/django/forms/how-to-use-bootstrap-4-in-django-forms/


def index(request: HttpRequest) -> HttpResponse:
    context = {}
    context['message'] = 'choose options'

    if request.method == 'POST':
        country = request.POST['country']
        state = request.POST['state']
        try:
            hotel_id = Hotel.objects.get(state=state, country=country).hotel_id
            return HttpResponseRedirect(f'/reservations/hotel/{hotel_id}')
        except Exception as err:
            context['form'] = HotelSelectionForm(initial={'country': 'US', 'state':'NJ'})
            context['message'] = 'no valid combination exists'
            return render(request, 'search.html', context )
    else:
        context['form'] = HotelSelectionForm(initial={'country': 'US', 'state':'NJ'})
        return render(request, 'search.html', context )


class ReservationView(View):
    def get(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]):
        initial = {}
        context = {}
        hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])
        initial['hotel'] = hotel

        form = ReservationForm(initial=initial)

        svcs = form.get_services(hotel)
        # form.fields['service'].choices = svcs
        form.fields['service'] = MultipleChoiceField(required=False, choices=svcs, widget=forms.CheckboxSelectMultiple())

        bkfst = form.get_breakfast(hotel)
        # form.fields['breakfast'].choices = bkfst
        form.fields['breakfast'] = EmptyChoiceField(required=False, choices=bkfst, widget=CheckboxInput()) # empty_label='---- none ----')

        user = request.user
        

        context['form'] = form



        return render(request, 'bookhotel.html', context)

    def post(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]):
        form = ReservationForm(request.POST)
        hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])

        svcs = form.get_services(hotel)
        form.fields['service'].choices = svcs

        bkfst = form.get_breakfast(hotel)
        form.fields['breakfast'].choices = bkfst

        context = {}
        messages = []
        context = {'form': form}
        if form.is_valid():
            if form.cleaned_data['check_in'] < datetime.datetime.today().date():
                messages.append('check in today or future')

            if form.cleaned_data['check_in'] >= form.cleaned_data['check_out']:
                messages.append('check out must be greater than check in')

            if len(messages) == 0:
                 return HttpResponse('you just booked a hotel room')

            context['messages'] = messages
            return render(request, 'bookhotel.html', context)

        else:
            messages.append('form is invalid')
            for e in form.errors:
                messages.append(e)

            context['messages'] = messages
        #hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])
        #initial = {'hotel' : hotel}

        return render(request, 'bookhotel.html', context)






