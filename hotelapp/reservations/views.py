from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from reservations.forms import HotelSelectionForm

from .models import Hotel

def index(request: HttpRequest) -> HttpResponse:
    context = {}
    context['message'] = 'choose options'

    if request.method == 'POST':
        country = request.POST['country']
        state = request.POST['state']

        try:
            hotel_id = Hotel.objects.get(state=state, country=country)
            return HttpResponse('Soon you can book a hotel')
        except:
            hotel_id = None
            context['form'] = HotelSelectionForm(initial={'country': 'US', 'state':'NJ'})
            context['message'] = 'no valid combination exists'

        # handle reading items and redirect to booking forms
        
    else:
        context['form'] = HotelSelectionForm(initial={'country': 'US', 'state':'NJ'})

    return render(request, 'search.html', context )