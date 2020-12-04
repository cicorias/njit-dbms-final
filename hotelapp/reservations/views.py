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
from datetime import date, timedelta
import datetime
import uuid
from reservations.fields import EmptyChoiceField, EmptyMultipleChoiceField

from users.models import CustomUser
from .forms import HotelSelectionForm, ReportForm, ReservationForm, ReviewForm

from .models import Breakfast, BreakfastReview, CreditCard, Hotel, Reservation, ReservationBreakfast, ReservationService, Room, RoomReservation, RoomReview, Service, BookingRequest, ServiceReview

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
    context = {}
    if request.method == 'POST':
        from  django.db import connection

        form = ReportForm(request.POST)
        if form.is_valid():
            parms = {'start': form.cleaned_data['start_date'], 'end': form.cleaned_data['end_date'] }
            if form.cleaned_data['report_type'] == '1':
                context['title'] = 'highest rated room'
                sql_stmt = '''
                    -- For a given time period (begin date and end date) compute the highest rated room type for each hotel.
                    SELECT
                        max(rating),
                        r.room_id,
                        r.hotel_id,
                        h.hotel_name
                    FROM
                        room_reservation rr
                        -- filter on these dates
                    JOIN room r on
                        rr.room_no = r.room_id
                    JOIN reservation resv on
                        rr.invoice_number = resv.invoice_number
                    JOIN customer c on
                        resv.cid = c.cid
                    JOIN room_review review on
                        review.cid = c.cid
                    JOIN hotel h on
                        r.hotel_id = h.hotel_id
                    WHERE
                        rr.check_in_date >= :start
                        AND rr.check_in_date <= :end
                    GROUP BY
                    h.hotel_name
                    '''

            elif form.cleaned_data['report_type'] == '2':
                context['title'] = 'five best customers'
                sql_stmt = '''
                        -- For a given time period (begin date and end date) compute the 5 best customers (in terms of money spent in reservations).
                        SELECT c.cid,c.friendly_name,sum(Total_Amount) as Amount
                        FROM (SELECT rv.cid,
                                r.price*(case when d.discount is null then 1
                                else d.discount
                            end)+ b.b_price + s.s_price as Total_Amount,
                                rv.invoice_number
                            FROM
                                room_reservation rr
                            JOIN rresv_breakfast rb on
                                rr.invoice_number = rb.rr_id
                            JOIN rresv_service rs on
                                rr.invoice_number = rs.rr_id
                            JOIN room r on
                                rr.hotel_id = r.hotel_id
                                and rr.room_no = r.room_no
                            JOIN (
                                SELECT
                                    r.room_id,
                                    d.discount
                                FROM
                                    discounted_room d
                                LEFT OUTER JOIN room r on
                                    d.room_id = r.room_id
                                WHERE
                                    d.start_date >= '2020-02-01'
                                    AND d.end_date <= '2021-02-01') d on
                                r.room_id = d.room_id
                            JOIN breakfast b on
                                rb.bid = b.bid
                            JOIN service s on
                                rs.sid = s.sid
                            JOIN reservation rv on
                                rv.invoice_number = rr.invoice_number
                            WHERE
                                rr.check_in_date >= '2020-02-01'
                                AND rr.check_out_date <= '2021-02-01'
                            ) as temp , customer c
                            where c.cid = temp.cid
                            GROUP BY c.cid 
                            ORDER BY
                                Amount desc
                            LIMIT 5;

                        '''

            elif form.cleaned_data['report_type'] == '3':
                context['title'] = 'highest rated breakfast'
                sql_stmt = '''
                    --- For a given time period (begin date and end date) compute the highest rated breakfast type across all hotels.
                    SELECT
                        max(rating),
                        b.b_type,
                        h.hotel_id,
                        h.hotel_name
                    FROM
                        room_reservation rr -- filter on dates
                    JOIN reservation resv on
                        rr.invoice_number = resv.invoice_number
                    JOIN rresv_breakfast rb on 
                        resv.invoice_number = rb.rr_id 
                    JOIN breakfast_review br on 
                        br.bid = rb.bid 
                    JOIN breakfast b on 
                        b.bid  == rb.bid 
                    JOIN hotel h on
                        rr.hotel_id = h.hotel_id
                    WHERE
                        rr.check_in_date >= :start
                        AND rr.check_in_date <= :end
                    '''

            elif  form.cleaned_data['report_type'] == '4':
                context['title'] = 'highest rated service'
                sql_stmt = '''
                    --- For a given time period (begin date and end date) compute the highest rated service type across all hotels.
                    SELECT
                        max(rating),
                        s.s_type,
                        h.hotel_id,
                        h.hotel_name
                    FROM
                        room_reservation rr -- filter on dates
                    JOIN reservation resv on
                        rr.invoice_number = resv.invoice_number
                    JOIN rresv_service resv on 
                        resv.invoice_number = rr.rr_id
                    JOIN service_review sr on 
                        resv.sid = sr.sid 
                    JOIN service s on 
                        s.sid  == sr.sid 
                    JOIN hotel h on
                        rr.hotel_id = h.hotel_id
                    WHERE
                        rr.check_in_date >= :start
                        AND rr.check_in_date <= :end
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
                cursor.execute(sql_stmt, parms)
                results = dictfetchall(cursor)
            
            context['results'] = results
            context['form'] = form
            return render(request, 'statistics.html', context)
    else:
        form = ReportForm()
        context['form'] = form
        return render(request, 'statistics.html', context)


class ReservationView(View):
    def get(self, request: HttpRequest, *args: Tuple, **kwargs: Dict[str, Any]):
        initial = {}
        context = {}
        hotel = get_object_or_404(Hotel, hotel_id=kwargs['hotel_id'])
        initial['hotel'] = hotel

        form = ReservationForm(initial=initial)

        # NOTE: refactor these fields - duplicate in POST body.
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

        # NOTE: refactor these fields
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
                    s_list,

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
                        br.rr_id = rr_resv # resv

                        br.save()

                    # services
                    for s in n_req.svc_id:
                        resv_svc = ReservationService()
                        resv_svc.sid = s
                        resv_svc.rr_id = rr_resv #  resv
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
    room_res_rv = {}
    room_svc_rv = {}
    room_bkfst_rv = {}

    resvs = request.user.reservation_set.all()
    
    for i in resvs:
        for j in i.roomreservation_set.all():
            room_res_rv[j.rr_id] = f'date: {i.r_date} - {j.hotel_id} - checkin: {j.check_in_date} through {j.check_out_date}'

            for k in j.reservationservice_set.all():
                room_svc_rv[k.rs_id] = f'date: {j.check_in_date} - {k.sid}'

            for k in j.reservationbreakfast_set.all():
                room_bkfst_rv[k.rb_id] = f'date: {j.check_in_date} - {k.bid}'
            

    context['reservations'] = room_res_rv
    context['services'] = room_svc_rv
    context['breakfasts'] = room_bkfst_rv

    return render(request, 'review_list.html', context)


def add_reviews(request: HttpRequest, type: str, id: int)-> HttpResponse:
    initial = {}
    context = {}

    if request.method == "POST":
        form = ReviewForm(request.POST)
        
        if type == 'reservation':
            hotel_id=RoomReservation.objects.get(rr_id=id).hotel_id_id
            hotel = get_object_or_404(Hotel,pk=hotel_id)
            room_no = RoomReservation.objects.get(rr_id=id).room_no_id
            #room = get_object_or_404(Room,room_no= room_no)

            room_res = get_object_or_404(RoomReservation, pk=id)
            
            roomreview, created = RoomReview.objects.get_or_create(cid=request.user, rr_id=room_res)

            if form.is_valid():
                roomreview.hotel_id = hotel
                roomreview.rr_id = room_res
                roomreview.rating = form.data['rating']
                roomreview.text_content = form.data['text']
                roomreview.cid = request.user

                roomreview.save()
                
                return HttpResponseRedirect(f'/reservations/review/')

        if type == 'service':
            svc_id = get_object_or_404(ReservationService,pk=id)
            servicereview, created = ServiceReview.objects.get_or_create(cid=request.user, sid=svc_id)

            if form.is_valid():
                servicereview.cid = request.user
                servicereview.sid = svc_id 
                servicereview.rating = form.data['rating']
                servicereview.text_content = form.data['text']
                servicereview.cid = request.user

                servicereview.save()

                return HttpResponseRedirect(f'/reservations/review')

        if type == 'breakfast':
            brk_id = get_object_or_404(ReservationBreakfast, pk=id)
            breakfastreview, created = BreakfastReview.objects.get_or_create(cid=request.user, bid=brk_id)

            if form.is_valid():
                breakfastreview.cid = request.user
                breakfastreview.bid = brk_id
                breakfastreview.rating = form.data['rating']
                breakfastreview.text_content = form.data['text']
                breakfastreview.cid = request.user

                breakfastreview.save()

                return HttpResponseRedirect(f'/reservations/review')


        return HttpResponse('something unexptected.')

    else :
        user = request.user
        initial['user'] = user
        form = ReviewForm(initial=initial)
        
        if type == 'reservation':
            room_reservations = form.get_room_reservations(user)
            values = room_reservations.get(id)
            form.fields['hotel_id'] = CharField(initial=values[0], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            form.fields['room_no'] = CharField(initial=values[1], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        if type == 'service':
            room_services = form.get_room_services(user)
            values = room_services.get(id)
            form.fields['reserviation_id'] = CharField(initial=values[0], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            form.fields['service'] = CharField(initial=values[1], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        if type == 'breakfast':
            room_breakfasts = form.get_room_breakfast(user)
            values = room_breakfasts.get(id)
            form.fields['reserviation_id'] = CharField(initial=values[0], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
            form.fields['breakfast'] = CharField(initial=values[1], required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

        context['form'] = form


    return render(request, 'add_reviews.html', context)
