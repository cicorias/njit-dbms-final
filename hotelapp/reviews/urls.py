from django.urls import path
from django.contrib.auth.decorators import login_required
from reviews.views import review_list,add_reviews

app_name = 'reviews'

urlpatterns = [
    path('', review_list, name='review_list' ),
    path('addreview', add_reviews, name='addreview'),
]    