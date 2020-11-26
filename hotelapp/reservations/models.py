from typing import cast
from django.db import models
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
# from django.contrib.admin.models import User
# Create your models here.
# Basically, django-profiles is for something else - it's just helping to create and manage user profiles across an application.
# First of all - you should link Contact models directly to the django.contrib.auth.models.User via ForeignKey. This way you can access given User's contacts by a simple query ie. User.contact_set.all() - it will return to you a list of User's contacts. This will also get rid off your error.
# Second - fields like first_name, last_name are already definied in django.contrib.auth.models.User, so there is no need to define them again in UserProfile. Read the source of User model here
# Third - if your user can only have one Profile and you're not intend to use very old versions of django then you should be using OneToOneField instead of ForeignKey.
# Fourth thing - you could probably omit usage of RequestContext() by using one of the generic views bundled with django - read about that here

# TODO: add __str__ functions to classes

# NOTE: CustomUser is in ./users/models.py
from users.models import CustomUser

class Hotel(models.Model):
  hotel_id =  models.AutoField(primary_key=True)
  street = models.CharField(max_length=40)
  country = models.CharField(max_length=40)
  state = models.CharField(max_length=20)
  zip = models.CharField(max_length=5)

  class Meta:
    db_table = 'hotel'


class Room(models.Model):
  STANDARD = 'standard'
  DOUBLE = 'double'
  DELUXE = 'deluxe'
  SUITE = 'suite'
  ROOM_TYPE_CHOICES = [(STANDARD, 'standard'), (DOUBLE,'double'), (DELUXE,'deluxe'), (SUITE, 'suite')]

  #real fields
  room_id = models.AutoField(primary_key=True)
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  room_no = models.CharField(max_length=10) # TODO might need to be composite
  room_type = models.CharField(choices=ROOM_TYPE_CHOICES,
                                max_length=20,
                                default=STANDARD)
  price = models.FloatField()
  description = models.CharField(max_length=40)
  floor = models.IntegerField()
  capacity = models.IntegerField()

  class Meta:
    db_table = 'room'
    constraints = [models.UniqueConstraint(
              fields=['hotel_id', 'room_no',], name='unique hotelroomid')
    ]


class CreditCard(models.Model):
  from datetime import datetime, timedelta

  VISA = 'visa'
  MASTERCARD = 'mastercard'
  AMEX = 'americanexpress'
  CC_CHOICES = [(VISA, 'visa'), (MASTERCARD,'mastercard'), (AMEX, 'american express')]

  #actual fields
  cc_number = models.AutoField(primary_key=True)
  cc_type = models.CharField(choices = CC_CHOICES, 
                              max_length = 20,
                              default=VISA)

  address = models.CharField(max_length=40)
  code = models.CharField(max_length=4) # amex is 4

  # expiration_date = models.DateField(default=datetime.now()+timedelta(days=30))
  expiration_date = models.DateField()
  name = models.CharField(max_length=40)

  def __str__(self):
    return f'{self.name} - {self.cc_type} - {self.cc_number}'

  class Meta:
    db_table = 'credit_card'


class Reservation(models.Model):
  invoice_number =  models.AutoField(primary_key=True)
  cid = models.ForeignKey(CustomUser, db_column='cid', on_delete=models.CASCADE)
  cc_number = models.ForeignKey(CreditCard, db_column='cc_number', on_delete=models.CASCADE)
  r_date = models.DateField()

  class Meta:
    db_table = 'reservation'


class RoomReservation(models.Model):
  rr_id = models.AutoField(primary_key=True)
  invoice_number = models.ForeignKey(Reservation, db_column='invoice_number', on_delete=CASCADE)
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  room_no = models.ForeignKey(Room, db_column='room_no', on_delete=CASCADE)
  check_in_date = models.DateField(db_column='check_in_date')
  check_out_date = models.DateField(db_column='check_out_date')

  class Meta:
    db_table = 'room_reservation'
    #unique_together = ()
    constraints = [models.UniqueConstraint(
                  fields=['invoice_number', 'hotel_id', 'room_no', 'check_in_date',], name='unique roomreservation')]

class Breakfast(models.Model):
  # types: continental, English, Italian, American, French
  CONTINENTAL = 'continental'
  ENGLISH = 'english'
  ITALIAN = 'italian'
  AMERICAN = 'american'
  FRENCH = 'french'
  BR_CHOICES = [(CONTINENTAL, 'continental'), (ENGLISH, 'english'), (ITALIAN, 'italian'), (AMERICAN, 'american'), (FRENCH, 'french')]

  #real fields
  bid = models.AutoField(primary_key=True)
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  b_type = models.CharField(choices=BR_CHOICES, max_length=20)
  b_price = models.FloatField()
  description = models.CharField(max_length=40)

  class Meta:
    db_table = 'breakfast'
    constraints = [models.UniqueConstraint(
                    fields=['hotel_id', 'b_type',], name='unique hotelbreakfasttype')]


class Service(models.Model):
  #parking, laundry, airport drop- off/pick up etc.)
  PARKING = 'parking'
  LAUNDRY = 'laundry'
  AIRPORT = 'airport'

  ST_CHOICES = [(PARKING, 'parking'), (LAUNDRY, 'laundry'),(AIRPORT, 'airport')]

  # real fields
  sid = models.AutoField(primary_key=True)
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  s_type = models.CharField(choices=ST_CHOICES, max_length=20)
  s_price = models.FloatField()

  class Meta:
    db_table = 'service'
    constraints = [models.UniqueConstraint(
                                  fields=['hotel_id', 's_type'], name='unique hotelservicetype')]



# TODO:
class ReservationBreakfast(models.Model):
  pass

class ReservationService(models.Model):
  pass

class DiscountedRoom(models.Model):
  pass

class RoomReview(models.Model):
  pass

class BreakfastReview(models.Model):
  pass

class ServiceReview(models.Model):
  pass