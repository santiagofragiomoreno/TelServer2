from django.db import models
from django.contrib.auth.models import User
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from django.utils import timezone


class Settings_forms(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True,unique=True)
    is_lastname = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_phone = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_city = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_import = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_origin = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_capacity = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_code = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_capacity = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_cancelation = models.BooleanField(default=True,db_index=False,blank=False,null=True)
    is_observation = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_pay = models.BooleanField(default=True, db_index=False,blank=False,null=True)

    class Meta:
        managed = True
        db_table = 'settings_forms'

    def __str__(self):
        return str(self.owner_user) + " - Apellido :" + self.is_name + " - Telefono :" + self.is_phone + " - Ciudad :" + self.is_city 
        + " - Importe :" + self.is_import

class Settings_alerts(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True,unique=True)
    max_temperature = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    min_temperature = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    start_time = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    end_time = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    max_capacity = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    listening_time = models.PositiveIntegerField(blank=True, null=True, db_index=True)

    class Meta:
        managed = True
        db_table = 'settings_alerts'

    def __str__(self):
        return str(self.owner_user)

class Payments(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True,unique=True)
    price_time = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    time_price = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    

    class Meta:
        managed = True
        db_table = 'payments'

    def __str__(self):
        return str(self.owner_user)

class Client (models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, db_index=True)
    lastname = models.CharField(max_length=1024, unique=False, null=True)
    birthdate = models.DateTimeField(unique=True, null=True)
    #created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.EmailField(blank=True, null=False)
    dni = models.CharField(max_length=1024, unique=False, null=True)
    tlf = models.PositiveIntegerField(max_length=1024, unique=False, null=True)
    direction = models.CharField(max_length=1024, unique=False, null=True)
    city = models.CharField(max_length=1024, unique=False, null=True)
    country = models.CharField(max_length=1024, unique=False, null=True)
    cp = models.CharField(max_length=1024, unique=False, null=True)

    class Meta:
        managed = True
        db_table = 'client'

    def __str__(self):
        return str(self.owner_user)

class Reservation(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True,unique=True,null=False)
    client = models.ForeignKey(Client, models.DO_NOTHING, db_index=True,unique=True,null=False)
    flat = models.ForeignKey(Flat, models.DO_NOTHING, db_index=True,unique=True,null=False)
    start_time = models.DateTimeField( unique=True, null=False)
    end_time = models.DateTimeField( unique=False, null=False)
    guest = models.PositiveIntegerField(max_length=1024, unique=False, null=True)

    class Meta:
        managed = True
        db_table = 'reservation'

    def __str__(self):
        return str(self.owner_user)