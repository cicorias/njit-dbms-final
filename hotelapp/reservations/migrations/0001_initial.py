# Generated by Django 3.1.3 on 2020-11-26 19:37

from django.conf import settings
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
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('b_type', models.CharField(choices=[('continental', 'continental'), ('english', 'english'), ('italian', 'italian'), ('american', 'american'), ('french', 'french')], max_length=20)),
                ('b_price', models.FloatField()),
                ('description', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'breakfast',
            },
        ),
        migrations.CreateModel(
            name='BreakfastReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('ccid', models.AutoField(primary_key=True, serialize=False)),
                ('cc_number', models.CharField(db_column='cc_number', max_length=20)),
                ('cc_type', models.CharField(choices=[('visa', 'visa'), ('mastercard', 'mastercard'), ('americanexpress', 'american express')], default='visa', max_length=20)),
                ('address', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=4)),
                ('expiration_date', models.DateField()),
                ('name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'credit_card',
            },
        ),
        migrations.CreateModel(
            name='DiscountedRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.AutoField(primary_key=True, serialize=False)),
                ('hotel_name', models.CharField(max_length=20)),
                ('street', models.CharField(max_length=40)),
                ('country', models.CharField(max_length=40)),
                ('state', models.CharField(max_length=20)),
                ('zip', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'hotel',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('invoice_number', models.AutoField(primary_key=True, serialize=False)),
                ('r_date', models.DateField()),
                ('cc_number', models.ForeignKey(db_column='cc_number', on_delete=django.db.models.deletion.CASCADE, to='reservations.creditcard')),
                ('cid', models.ForeignKey(db_column='cid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
        migrations.CreateModel(
            name='ReservationBreakfast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.AutoField(primary_key=True, serialize=False)),
                ('room_no', models.CharField(max_length=10)),
                ('room_type', models.CharField(choices=[('standard', 'standard'), ('double', 'double'), ('deluxe', 'deluxe'), ('suite', 'suite')], default='standard', max_length=20)),
                ('price', models.FloatField()),
                ('description', models.CharField(max_length=40)),
                ('floor', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel')),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='RoomReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('s_type', models.CharField(choices=[('parking', 'parking'), ('laundry', 'laundry'), ('airport', 'airport')], max_length=20)),
                ('s_price', models.FloatField()),
                ('hotel_id', models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel')),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('rr_id', models.AutoField(primary_key=True, serialize=False)),
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
        migrations.AddConstraint(
            model_name='creditcard',
            constraint=models.UniqueConstraint(fields=('cc_number',), name='unique creditcard'),
        ),
        migrations.AddField(
            model_name='breakfast',
            name='hotel_id',
            field=models.ForeignKey(db_column='hotel_id', on_delete=django.db.models.deletion.CASCADE, to='reservations.hotel'),
        ),
        migrations.AddConstraint(
            model_name='service',
            constraint=models.UniqueConstraint(fields=('hotel_id', 's_type'), name='unique hotelservicetype'),
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
            model_name='breakfast',
            constraint=models.UniqueConstraint(fields=('hotel_id', 'b_type'), name='unique hotelbreakfasttype'),
        ),
    ]
