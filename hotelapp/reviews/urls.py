from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list' ),
]    