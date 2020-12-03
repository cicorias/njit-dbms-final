# Generated by Django 3.1.3 on 2020-12-03 01:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breakfast',
            fields=[
                ('bid', models.AutoField(db_column='bid', primary_key=True, serialize=False)),
                ('b_type', models.CharField(choices=[('continental', 'continental'), ('english', 'english'), ('italian', 'italian'), ('american', 'american'), ('french', 'french')], db_column='b_type', max_length=20)),
                ('b_price', models.FloatField(db_column='b_price')),
                ('description', models.CharField(db_column='description', max_length=40)),
            ],
            options={
                'db_table': 'breakfast',
            },
        ),
        migrations.CreateModel(
            name='BreakfastReview',
            fields=[
                ('rid', models.AutoField(db_column='rid', primary_key=True, serialize=False)),
                ('review_date', models.DateField(auto_now_add=True, db_column='review_date')),
                ('rating', models.PositiveIntegerField(db_column='rating', default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('text_content', models.CharField(db_column='text', max_length=40)),
            ],
            options={
                'db_table': 'breakfast_review',
            },
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('ccid', models.AutoField(db_column='ccid', primary_key=True, serialize=False)),
                ('cc_number', models.CharField(db_column='cc_number', max_length=20)),
                ('cc_type', models.CharField(choices=[('visa', 'visa'), ('mastercard', 'mastercard'), ('americanexpress', 'american express')], db_column='cc_type', default='visa', max_length=20)),
                ('address', models.CharField(db_column='address', max_length=40)),
                ('cv_code', models.CharField(db_column='cv_code', max_length=4)),
                ('expiration_date', models.DateField(db_column='exp_date')),
                ('name', models.CharField(db_column='name', max_length=40)),
            ],
            options={
                'db_table': 'credit_card',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.AutoField(db_column='hotel_id', primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(db_column='hotel_name', max_length=20)),
                ('street', models.CharField(db_column='street', max_length=40)),
                ('country', models.CharField(db_column='country', max_length=40)),
                ('state', models.CharField(db_column='state', max_length=20)),
                ('zip', models.CharField(db_column='zip', max_length=5)),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('invoice_number', models.AutoField(db_column='invoice_number', primary_key=True, serialize=False)),
                ('r_date', models.DateField(db_column='r_date')),
                ('cc_number', models.ForeignKey(db_column='cc_number', on_delete=django.db.models.deletion.CASCADE, to='reservations.creditcard')),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
        migrations.CreateModel(
            name='ReservationService',
            fields=[
                ('rs_id', models.AutoField(db_column='rs_id', primary_key=True, serialize=False)),
                ('sprice', models.FloatField(db_column='sprice')),
                ('rr_id', models.ForeignKey(db_column='rr_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
            ],
            options={
                'db_table': 'rresv_service',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(db_column='room_id', primary_key=True, serialize=False)),
                ('room_no', models.CharField(db_column='room_no', max_length=10)),
                ('room_type', models.CharField(choices=[('standard', 'standard'), ('double', 'double'), ('deluxe', 'deluxe'), ('suite', 'suite')], db_column='room_type', default='standard', max_length=20)),
                ('price', models.FloatField(db_column='price')),
                ('description', models.CharField(db_column='description', max_length=40)),
                ('floor', models.PositiveIntegerField(db_column='floor')),
                ('capacity', models.PositiveIntegerField(db_column='capacity')),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel')),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('rid', models.AutoField(db_column='rid', primary_key=True, serialize=False)),
                ('review_date', models.DateField(auto_now_add=True, db_column='review_date')),
                ('rating', models.PositiveIntegerField(db_column='rating', default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('text_content', models.CharField(db_column='text', max_length=40)),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sid', models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.CASCADE, to='reservations.reservationservice')),
            ],
            options={
                'db_table': 'service_review',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('sid', models.AutoField(db_column='sid', primary_key=True, serialize=False)),
                ('s_type', models.CharField(choices=[('parking', 'parking'), ('laundry', 'laundry'), ('airport', 'airport')], db_column='s_type', max_length=20)),
                ('s_price', models.FloatField(db_column='s_price')),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel')),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='RoomReview',
            fields=[
                ('rid', models.AutoField(db_column='rid', primary_key=True, serialize=False)),
                ('review_date', models.DateField(auto_now_add=True, db_column='review_date', null=True)),
                ('rating', models.PositiveIntegerField(db_column='rating', default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('text_content', models.CharField(db_column='text', max_length=40)),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room_id', models.ForeignKey(db_column='room_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.room')),
            ],
            options={
                'db_table': 'room_review',
            },
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('rr_id', models.AutoField(db_column='rr_id', primary_key=True, serialize=False)),
                ('check_in_date', models.DateField(db_column='check_in_date')),
                ('check_out_date', models.DateField(db_column='check_out_date')),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel')),
                ('invoice_number', models.ForeignKey(db_column='invoice_number', on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
                ('room_no', models.ForeignKey(db_column='room_no', on_delete=django.db.models.deletion.CASCADE, to='reservations.room')),
            ],
            options={
                'db_table': 'room_reservation',
            },
        ),
        migrations.AddField(
            model_name='reservationservice',
            name='sid',
            field=models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.CASCADE, to='reservations.service'),
        ),
        migrations.CreateModel(
            name='ReservationBreakfast',
            fields=[
                ('rb_id', models.AutoField(db_column='rb_id', primary_key=True, serialize=False)),
                ('nooforders', models.PositiveIntegerField(db_column='nooforders')),
                ('bid', models.ForeignKey(db_column='bid', on_delete=django.db.models.deletion.CASCADE, to='reservations.breakfast')),
                ('rr_id', models.ForeignKey(db_column='rr_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation')),
            ],
            options={
                'db_table': 'rresv_breakfast',
            },
        ),
        migrations.CreateModel(
            name='DiscountedRoom',
            fields=[
                ('dr_id', models.AutoField(db_column='dr_id', primary_key=True, serialize=False)),
                ('discount', models.FloatField(db_column='discount')),
                ('start_date', models.DateField(db_column='start_date')),
                ('end_date', models.DateField(db_column='end_date')),
                ('room_id', models.ForeignKey(db_column='room_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.room')),
            ],
            options={
                'db_table': 'discounted_room',
            },
        ),
        migrations.AddConstraint(
            model_name='creditcard',
            constraint=models.UniqueConstraint(fields=('cc_number',), name='unique creditcard'),
        ),
        migrations.AddField(
            model_name='breakfastreview',
            name='bid',
            field=models.ForeignKey(db_column='bid', on_delete=django.db.models.deletion.CASCADE, to='reservations.reservationbreakfast'),
        ),
        migrations.AddField(
            model_name='breakfastreview',
            name='cid',
            field=models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='breakfast',
            name='hotel_id',
            field=models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel'),
        ),
        migrations.AddConstraint(
            model_name='servicereview',
            constraint=models.UniqueConstraint(fields=('cid', 'sid'), name='unique servicereview'),
        ),
        migrations.AddConstraint(
            model_name='service',
            constraint=models.UniqueConstraint(fields=('hotel_id', 's_type'), name='unique hotelservicetype'),
        ),
        migrations.AddConstraint(
            model_name='roomreview',
            constraint=models.UniqueConstraint(fields=('cid', 'room_id'), name='unique roomreview'),
        ),
        migrations.AddConstraint(
            model_name='roomreservation',
            constraint=models.UniqueConstraint(fields=('invoice_number', 'hotel_id', 'room_no', 'check_in_date'), name='unique roomreservation'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('hotel_id', 'room_no'), name='unique hotelroomid'),
        ),
        migrations.AddConstraint(
            model_name='reservationservice',
            constraint=models.UniqueConstraint(fields=('sid', 'rr_id'), name='unique roomresservice'),
        ),
        migrations.AddConstraint(
            model_name='reservationbreakfast',
            constraint=models.UniqueConstraint(fields=('bid', 'rr_id'), name='unique roomresbreakfast'),
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.UniqueConstraint(fields=('cc_number', 'r_date'), name='unique reservation'),
        ),
        migrations.AddConstraint(
            model_name='breakfastreview',
            constraint=models.UniqueConstraint(fields=('cid', 'bid'), name='unique breakfastreview'),
        ),
        migrations.AddConstraint(
            model_name='breakfast',
            constraint=models.UniqueConstraint(fields=('hotel_id', 'b_type'), name='unique hotelbreakfasttype'),
        ),
    ]
