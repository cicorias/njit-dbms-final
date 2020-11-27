from django.forms import ModelForm

from .models import Hotel, Reservation


# https://stackoverflow.com/questions/14901680/how-to-do-a-multi-step-form-in-django/14901714#14901714
# https://github.com/jazzband/django-formtools
# https://django-formtools.readthedocs.io/en/latest/wizard.html


# adding to model admin site https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

class ReservationForm(ModelForm):
    pass