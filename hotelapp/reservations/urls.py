from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'reservations'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('', login_required(views.SurveyList.as_view(
    #         template_name='survey_list.html'))),
    path('', views.index, name='index' ),
]