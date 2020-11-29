from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index' ),
    path('hotel/<hotel_id>', login_required(views.ReservationView.as_view(), login_url='/users/login'), name='book-hotel'),
    path('bookings/', login_required(views.bookings, login_url='/users/login'), name='bookings'),
    path('stats/highestratedroom', login_required(views.stats_highest_rated_room, login_url='/users/login'), name='stats_highest_rated_room'),

]