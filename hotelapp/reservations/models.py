import datetime
from typing import NamedTuple, cast
from collections import namedtuple
from django.db import models
from django.db.models import constraints
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator 

# NOTE: CustomUser is in ./users/models.py
from users.models import CustomUser

class Hotel(models.Model):
  hotel_id =  models.AutoField(primary_key=True, db_column='hotel_id')
  hotel_name = models.CharField(max_length=20, db_column='hotel_name')
  street = models.CharField(max_length=40, db_column='street')
  country = models.CharField(max_length=40, db_column='country')
  state = models.CharField(max_length=20, db_column='state')
  zip = models.CharField(max_length=5, db_column='zip')

  def __str__(self) -> str:
    return f'{self.hotel_id} - {self.hotel_name} - {self.country}'

  class Meta:
    db_table = 'hotel'


class Room(models.Model):
  STANDARD = 'standard'
  DOUBLE = 'double'
  DELUXE = 'deluxe'
  SUITE = 'suite'
  ROOM_TYPE_CHOICES = [(STANDARD, 'standard'), (DOUBLE,'double'), (DELUXE,'deluxe'), (SUITE, 'suite')]

  #real fields
  room_id = models.AutoField(primary_key=True, db_column='room_id')
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  room_no = models.CharField(max_length=10, db_column='room_no')
  room_type = models.CharField(choices=ROOM_TYPE_CHOICES,
                                db_column='room_type',
                                max_length=20,
                                default=STANDARD)
  price = models.FloatField(db_column='price')
  description = models.CharField(max_length=40, db_column='description')
  floor = models.PositiveIntegerField(db_column='floor')
  capacity = models.PositiveIntegerField(db_column='capacity')

  def __str__(self) -> str:
    return f'{self.hotel_id} - room {self.room_no}'

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
  ccid = models.AutoField(primary_key=True, db_column='ccid')
  cc_number = models.CharField(db_column='cc_number', max_length=20)
  cc_type = models.CharField(choices = CC_CHOICES,
                              db_column='cc_type',
                              max_length = 20,
                              default=VISA)

  address = models.CharField(max_length=40, db_column='address')
  cv_code = models.CharField(max_length=4, db_column='cv_code')

  # expiration_date = models.DateField(default=datetime.now()+timedelta(days=30))
  expiration_date = models.DateField(db_column='exp_date')
  name = models.CharField(max_length=40, db_column='name')

  def __str__(self):
    return f'{self.name} - {self.cc_type} - {self.cc_number}'

  class Meta:
    db_table = 'credit_card'
    constraints = [models.UniqueConstraint(fields=['cc_number'], name='unique creditcard')]


class Reservation(models.Model):
  invoice_number =  models.AutoField(primary_key=True, db_column='invoice_number')
  cid = models.ForeignKey(CustomUser, 
                        db_column='cid',
                        on_delete=models.CASCADE)
  cc_number = models.ForeignKey(CreditCard, 
                        db_column='cc_number',
                        on_delete=models.CASCADE)
  r_date = models.DateField(db_column='r_date')

  def __str__(self) -> str:
    return f'{self.cid} - {self.invoice_number}'

  class Meta:
    db_table = 'reservation'
    constraints = [models.UniqueConstraint(
              fields=['cc_number', 'r_date'], name='unique reservation')]


class RoomReservation(models.Model):
  rr_id = models.AutoField(primary_key=True, db_column='rr_id')
  invoice_number = models.ForeignKey(Reservation, db_column='invoice_number', on_delete=CASCADE)
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  room_no = models.ForeignKey(Room, db_column='room_no', on_delete=CASCADE)
  check_in_date = models.DateField(db_column='check_in_date')
  check_out_date = models.DateField(db_column='check_out_date')

  def __str__(self) -> str:
    return f'{self.hotel_id}:{self.room_no} rr_id: {self.rr_id}'

  class Meta:
    db_table = 'room_reservation'
    constraints = [models.UniqueConstraint(
                  fields=['invoice_number',
                          'hotel_id',
                          'room_no',
                          'check_in_date',], 
                          name='unique roomreservation')]

class Breakfast(models.Model):
  # types: continental, English, Italian, American, French
  CONTINENTAL = 'continental'
  ENGLISH = 'english'
  ITALIAN = 'italian'
  AMERICAN = 'american'
  FRENCH = 'french'
  BR_CHOICES = [(CONTINENTAL, 'continental'), (ENGLISH, 'english'), (ITALIAN, 'italian'), (AMERICAN, 'american'), (FRENCH, 'french')]

  #real fields
  bid = models.AutoField(primary_key=True, db_column='bid')
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  b_type = models.CharField(choices=BR_CHOICES,
                            db_column='b_type',
                            max_length=20)
  b_price = models.FloatField(db_column='b_price')
  description = models.CharField(max_length=40, db_column='description')

  def __str__(self) -> str:
    return f'{self.hotel_id}:{self.b_type}: {self.description} - bid: {self.bid}'

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
  sid = models.AutoField(primary_key=True, db_column='sid')
  hotel_id = models.ForeignKey(Hotel, db_column='hotel_id', on_delete=CASCADE)
  s_type = models.CharField(choices=ST_CHOICES,
                            db_column='s_type',
                            max_length=20)
  s_price = models.FloatField(db_column='s_price')

  def __str__(self) -> str:
    return f'{self.hotel_id}:{self.s_type} - sid: {self.sid}'

  class Meta:
    db_table = 'service'
    constraints = [models.UniqueConstraint(
                          fields=['hotel_id', 's_type'], name='unique hotelservicetype')]


class ReservationBreakfast(models.Model):
  rb_id = models.AutoField(primary_key=True, db_column='rb_id')
  bid = models.ForeignKey(Breakfast, db_column='bid', on_delete=CASCADE)
  rr_id = models.ForeignKey(Reservation, db_column='rr_id', on_delete=CASCADE)

  nooforders = models.PositiveIntegerField(db_column='nooforders')

  def __str__(self) -> str:
    return f'{self.bid}:{self.rr_id} - rb_id:{self.rb_id}'

  class Meta:
    db_table = 'rresv_breakfast'
    constraints = [models.UniqueConstraint(
                fields=['bid','rr_id'], name='unique roomresbreakfast')]


class ReservationService(models.Model):
  rs_id = models.AutoField(primary_key=True, db_column='rs_id')
  sid = models.ForeignKey(Service, db_column='sid', on_delete=CASCADE)
  rr_id = models.ForeignKey(Reservation, db_column='rr_id', on_delete=CASCADE)

  # TODO: remove this as it is in the service definition
  sprice = models.FloatField(db_column='sprice')

  def __str__(self) -> str:
    return f'{self.sid}:{self.rr_id} - rs_id:{self.rs_id}'

  class Meta:
    db_table = 'rresv_service'
    constraints = [models.UniqueConstraint(
                  fields=['sid', 'rr_id'], name='unique roomresservice')]


class DiscountedRoom(models.Model):
  dr_id = models.AutoField(primary_key=True, db_column='dr_id')
  room_id = models.ForeignKey(Room, db_column='room_id', on_delete=CASCADE)

  discount = models.FloatField(db_column='discount')
  start_date = models.DateField(db_column='start_date')
  end_date = models.DateField(db_column='end_date')

  def __str__(self) -> str:
    return f'{self.room_id}'

  class Meta:
    db_table = 'discounted_room'
    # TODO: are discounts unique by date too?


class RoomReview(models.Model):
  rid = models.AutoField(primary_key=True, db_column='rid')
  cid = models.ForeignKey(CustomUser, db_column='cid', on_delete=CASCADE)
  room_id = models.ForeignKey(Room, db_column='room_id', on_delete=CASCADE)
  review_date = models.DateField(db_column='review_data', default=datetime.date.today)

  rating = models.PositiveIntegerField(db_column='rating',
            default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
  text_content = models.CharField(max_length=40, db_column='text')

  def __str__(self) -> str:
    return f'{self.room_id} - rid: {self.rid}'

  class Meta:
    db_table = 'room_review'
    constraints = [models.UniqueConstraint(
              fields=['cid', 'room_id'],
              name='unique roomreview'
    )]  


class BreakfastReview(models.Model):
  rid = models.AutoField(primary_key=True, db_column='rid')
  cid = models.ForeignKey(CustomUser, db_column='cid', on_delete=CASCADE)
  bid = models.ForeignKey(Breakfast, db_column='bid', on_delete=CASCADE)
  review_date = models.DateField(db_column='review_data', default=datetime.date.today)

  rating = models.PositiveIntegerField(db_column='rating',
            default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
  text_content = models.CharField(max_length=40, db_column='text')

  def __str__(self) -> str:
    return f'{self.cid}: {self.bid} - rid:{self.rid}'

  class Meta:
    db_table = 'breakfast_review'
    constraints = [models.UniqueConstraint(
          fields=['cid', 'bid'],
          name='unique breakfastreview'
    )]


class ServiceReview(models.Model):
  rid = models.AutoField(primary_key=True, db_column='rid')
  cid = models.ForeignKey(CustomUser, db_column='cid', on_delete=CASCADE)
  sid = models.ForeignKey(Service, db_column='sid', on_delete=CASCADE)
  review_date = models.DateField(db_column='review_data', default=datetime.date.today)

  rating = models.PositiveIntegerField(db_column='rating',
          default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
  text_content = models.CharField(max_length=40, db_column='text')

  def __str__(self) -> str:
    return f'{self.sid} from {self.cid}  - rid: {self.rid}'

  class Meta:
    db_table = 'service_review'
    constraints = [models.UniqueConstraint(
          fields=['cid', 'sid'],
          name='unique servicereview'
    )]


# non classes form DTO to pass around...
BookingRequest = namedtuple('BookingReqeust',
          ['hotel', 
          'room',
          'credit_card_number',
          'credit_card_type',
          'credit_card_month',
          'credit_card_year',
          'credit_card_code',
          'credit_card_address',
          'credit_card_name',
          'cust_id',
          'res_date',
          'check_in',
          'check_out',
          'breakfast',
          'breakfast_number_orders',
          'svc_id', # TODO
          # 'discount_id', # TODO
          ])