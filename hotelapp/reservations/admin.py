from django.contrib import admin

# Register your models here.
from .models import DiscountedRoom, Hotel, ReservationService, Room, CreditCard, Reservation, RoomReservation, \
        Breakfast, RoomReview, Service, BreakfastReview, ServiceReview, ReservationBreakfast


admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(CreditCard)
admin.site.register(Reservation)
admin.site.register(RoomReservation)
admin.site.register(Breakfast)
admin.site.register(Service)
admin.site.register(DiscountedRoom)
admin.site.register(RoomReview)
admin.site.register(BreakfastReview)
admin.site.register(ServiceReview)
admin.site.register(ReservationBreakfast)
admin.site.register(ReservationService)

