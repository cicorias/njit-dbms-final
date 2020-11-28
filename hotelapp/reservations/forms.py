from django import forms
from django.forms import fields
#from django.forms import Form, ModelForm

from .models import Hotel, Reservation


# https://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django/14901714#14901714
# https://github.com/jazzband/django-formtools
# https://django-formtools.readthedocs.io/en/latest/wizard.html


# adding to model admin site https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

class ReservationForm(forms.ModelForm):
    pass

class HotelSelectionForm(forms.Form):
    country = forms.CharField(label = 'country', max_length=20)
    state = forms.CharField(label = 'state')

# class HotelSelectionForm(forms.ModelForm):
#     class Meta:
#         model = Hotel
#         fields = ['country', 'state']

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
