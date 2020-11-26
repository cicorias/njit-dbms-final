from django.contrib import admin

# Register your models here.
from reservations.models import Hotel, Room, CreditCard, Reservation, RoomReservation, Breakfast, Service, BreakfastReview, ServiceReview

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(CreditCard)
admin.site.register(Reservation)
admin.site.register(RoomReservation)
admin.site.register(Breakfast)
admin.site.register(Service)