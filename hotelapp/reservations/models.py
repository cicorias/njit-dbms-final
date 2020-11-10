from django.db import models
# from django.contrib.admin.models import User
# Create your models here.
# Basically, django-profiles is for something else - it's just helping to create and manage user profiles across an application.
# First of all - you should link Contact models directly to the django.contrib.auth.models.User via ForeignKey. This way you can access given User's contacts by a simple query ie. User.contact_set.all() - it will return to you a list of User's contacts. This will also get rid off your error.
# Second - fields like first_name, last_name are already definied in django.contrib.auth.models.User, so there is no need to define them again in UserProfile. Read the source of User model here
# Third - if your user can only have one Profile and you're not intend to use very old versions of django then you should be using OneToOneField instead of ForeignKey.
# Fourth thing - you could probably omit usage of RequestContext() by using one of the generic views bundled with django - read about that here


# NOTE: CustomUser is in ./users/models.py
from users.models import CustomUser

class Hotel(models.Model):
  hotel_id =  models.AutoField(primary_key=True)
  street = models.CharField(max_length=40)
  country = models.CharField(max_length=40)
  state = models.CharField(max_length=20)
  zip = models.CharField(max_length=5)

class CreditCard(models.Model):
  cc_number = models.AutoField(primary_key=True)

class Reservation(models.Model):
  invoice_number =  models.AutoField(primary_key=True)
  cid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  cc_number = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
  r_date = models.DateField()
