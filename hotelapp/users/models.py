from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    cid = models.AutoField(db_column='cid', primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    friendly_name = models.CharField(max_length=40, default='NA')
    address = models.CharField(max_length=40, default='NA')
    phone = models.CharField(max_length=40, default='NA')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'customer'
