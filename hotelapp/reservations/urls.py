from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.index, name='index' ),
    path('hotel/<hotel_id>', login_required(views.ReservationView.as_view(), login_url='/users/login'), name='book-hotel'),
    path('bookings/', login_required(views.bookings, login_url='/users/login'), name='bookings'),
    path('review/', login_required(views.review_list, login_url='/users/login'), name='review'),
    path('review/addreview/<str:type>/<int:id>', login_required(views.add_reviews, login_url='/users/login'), name='addreview'),
    path('stats/', login_required(views.general_statistics, login_url='/users/login'), name='stats'),
    path('stats/highestratedroom', login_required(views.general_statistics, login_url='/users/login'), name='stats_highest_rated_room'),
    path('stats/fivebestcustomers', login_required(views.general_statistics, login_url='/users/login'), name='stats_five_best_customers'),
    path('stats/highestratedbreakfast', login_required(views.general_statistics, login_url='/users/login'), name='stats_highest_rated_breakfast'),
    path('stats/highestratedservice', login_required(views.general_statistics, login_url='/users/login'), name='stats_highest_rated_service'),
]