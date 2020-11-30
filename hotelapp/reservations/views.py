from typing import Any, Dict, Tuple
from django.forms.fields import CharField, ChoiceField, MultipleChoiceField
from django.forms.widgets import CheckboxInput
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.views.generic import View, TemplateView
from django import forms
from django.db import connection, transaction
from datetime import timedelta
import datetime
import uuid
from reservations.fields import EmptyChoiceField, EmptyMultipleChoiceField

from users.models import CustomUser
from .forms import HotelSelectionForm, ReservationForm, ReviewForm

from .models import Breakfast, CreditCard, Hotel, Reservation, ReservationBreakfast, ReservationService, Room, RoomReservation, RoomReview, Service, BookingRequest

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

def bookings(request: HttpRequest) -> HttpResponse:
    context = {}
    rv = {}
    resvs = request.user.reservation_set.all()
    for i in resvs:
        for j in i.roomreservation_set.all():
            rv[j] = f'date: {i.r_date} - {j.hotel_id} - checkin: {j.check_in_date} through {j.check_out_date}'

    context['reservations'] = rv #  [(k, v) for k, v in rv.items()]
    return render(request, 'bookings.html', context)

def general_statistics(request: HttpRequest) -> HttpResponse:
    from  django.db import connection
    context = {}

    if 'highestratedroom' in request.path:
        context['title'] = 'highest rated room'
        sql_stmt = '''
            SELECT max(rating), r.room_id, r.hotel_id, h.hotel_name 
            FROM room_review rr
            JOIN room r on rr.room_id = r.room_id
            JOIN hotel h on r.hotel_id = r.hotel_id
            GROUP BY h.hotel_name 
            '''

    elif 'fivebestcustomers' in request.path:
        context['title'] = 'five best customers'
        sql_stmt = 'select "foobar"'

    elif 'highestratedbreakfast' in request.path:
        context['title'] = 'highest rated breakfast'
        sql_stmt = '''
            SELECT max(rating), bb.b_type 
            FROM breakfast_review br
            JOIN breakfast bb on br.bid = bb.bid 
            '''

    elif 'highestratedservice' in request.path:
        context['title'] = 'highest rated service'
        sql_stmt = '''
            SELECT max(rating), s.s_type 
            FROM service_review sr
            JOIN service s on sr.sid = s.sid 
            '''

    else:
        sql_stmt = 'SELECT "foobar"'

    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    with connection.cursor() as cursor:
        cursor.execute(sql_stmt)

        results = dictfetchall(cursor)
    
    context['results'] = results
    return render(request, 'statistics.html', context)


class ReservationView(View):
    def get(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]):
        initial = {}
        context = {}
        hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])
        initial['hotel'] = hotel

        form = ReservationForm(initial=initial)

        # TODO: refactor these fields - duplicate in POST body.
        svcs = form.get_services(hotel)
        form.fields['service'] = MultipleChoiceField(required=False, choices=svcs, widget=forms.CheckboxSelectMultiple())

        bkfst = form.get_breakfast(hotel)
        form.fields['breakfast'] = EmptyChoiceField(required=False, choices=bkfst, empty_label='---- none ----') #, widget=CheckboxInput()) # 

        rooms = form.get_rooms(hotel)
        form.fields['room_choice'] = ChoiceField(required=True, choices=rooms)

        if len(rooms) > 0:
            disc = form.get_discounts(rooms[0][0], form.fields['check_in'], form.fields['check_out'])
            form.fields['discount'] = CharField(initial=disc, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        # END refactor
        
        user = request.user
        context['form'] = form

        return render(request, 'bookhotel.html', context)

    def post(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]):
        form = ReservationForm(request.POST)
        hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])

        # TODO: refactor these fields
        svcs = form.get_services(hotel)
        form.fields['service'] = MultipleChoiceField(required=False, choices=svcs, widget=forms.CheckboxSelectMultiple())

        bkfst = form.get_breakfast(hotel)
        form.fields['breakfast'] = EmptyChoiceField(required=False, choices=bkfst, empty_label='---- none ----') #, widget=CheckboxInput()) # 

        rooms = form.get_rooms(hotel)
        form.fields['room_choice'] = ChoiceField(required=True, choices=rooms)

        if len(rooms) > 0:
            disc = form.get_discounts(rooms[0][0], form.fields['check_in'], form.fields['check_out'])
            form.fields['discount'] = CharField(initial=disc, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
        # END refactor

        user = request.user
        context = {}
        messages = []
        context = {'form': form}
        if form.is_valid():
            if form.cleaned_data['check_in'] < datetime.datetime.today().date():
                messages.append('check in today or future')

            if form.cleaned_data['check_in'] >= form.cleaned_data['check_out']:
                messages.append('check out must be greater than check in')

            # checks: cc date in future
            cc_exp_date = datetime.date(int(form.cleaned_data['credit_card_year']), int(form.cleaned_data['credit_card_month']), 1)
            if cc_exp_date < datetime.date.today():
                messages.append('credit card date must be greater than today')


            # we can now persist.
            if len(messages) == 0:

                s_list = []
                for s in form.cleaned_data['service']:
                    s_list.append(Service.objects.get(pk=s))

                new_booking = BookingRequest(
                    hotel,
                    form.cleaned_data['room_choice'],
                    form.cleaned_data['credit_card_number'],
                    form.cleaned_data['credit_card_type'],
                    form.cleaned_data['credit_card_month'],
                    form.cleaned_data['credit_card_year'],
                    form.cleaned_data['credit_card_code'],
                    form.cleaned_data['credit_card_address'],
                    form.cleaned_data['credit_card_name'],
                    request.user,
                    datetime.date.today(),
                    form.cleaned_data['check_in'],
                    form.cleaned_data['check_out'],
                    form.cleaned_data['breakfast'],
                    form.cleaned_data['breakfast_number_orders'],
                    s_list, # TODO - a list
                    # form.cleaned_data['discount_id'] # TODO

                )
                
                # order of saving:
                # 1. credit card x
                # 2. reservation x
                # 3. room_reservation x
                # 4. rresb_breakfast x
                # 5. rresv_service x

                @transaction.atomic
                def save_reservation(n_req: BookingRequest):

                    card = CreditCard()
                    card.address = n_req.credit_card_address
                    card.cc_number = n_req.credit_card_number
                    card.cc_type = n_req.credit_card_type
                    card.cv_code = n_req.credit_card_code
                    exp_date = datetime.date(int(n_req.credit_card_year), int(n_req.credit_card_month), 1)
                    card.expiration_date = exp_date

                    card.save()

                    resv = Reservation()
                    resv.cid = n_req.cust_id
                    resv.r_date = n_req.res_date
                    # grab the key
                    resv.cc_number = card
                    
                    resv.save()

                    room = Room.objects.get(pk=n_req.room)
                    rr_resv = RoomReservation()
                    rr_resv.check_in_date = n_req.check_in
                    rr_resv.check_out_date = n_req.check_out
                    rr_resv.hotel_id = n_req.hotel
                    # grab the key
                    rr_resv.room_no = room
                    rr_resv.invoice_number = resv

                    rr_resv.save()

                    # breakfast
                    if len(n_req.breakfast) > 0:
                        br = ReservationBreakfast()
                        br.bid = Breakfast.objects.get(pk=n_req.breakfast)
                        br.nooforders = n_req.breakfast_number_orders
                        br.rr_id = resv

                        br.save()

                    # services
                    for s in n_req.svc_id:
                        resv_svc = ReservationService()
                        resv_svc.sid = s
                        resv_svc.rr_id = resv
                        resv_svc.sprice = s.s_price

                        resv_svc.save()


                save_reservation(new_booking)

                return HttpResponseRedirect(f'/reservations/bookings/')

            context['messages'] = messages
            return render(request, 'bookhotel.html', context)

        else:
            messages.append('form is invalid')
            for e in form.errors:
                messages.append(e)

            context['messages'] = messages

        return render(request, 'bookhotel.html', context)


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
    initial = {}
    context = {}
    if request.method == "GET":
        user = request.user
        initial['user'] = user
        form = ReviewForm(initial=initial)

        # TODO: since this user is logged on we can use request.
        room_reservations = form.get_room_reservations(request.user).values()
        for v in room_reservations:
            val = room_reservations[v]
            form.fields[val] = ChoiceField(required=True, choices=val)
            

        form.get_room_number

        context['form'] = form

    return render(request, 'add_reviews.html', context)