from django.shortcuts import render,get_object_or_404
from reservations.models import RoomReview,RoomReservation,Reservation
from users.models import CustomUser

# Create your views here.

def review_list(request):
    cid = CustomUser.objects.get(email=request.user.email).cid
    reservation_invoices = Reservation.objects.all()
    room_reservations = []
    for invoice in reservation_invoices:
        room_reservations.append(RoomReservation.objects.get(invoice_number=invoice))
    return render(request,'review_list.html',{'room_reservations': room_reservations})

