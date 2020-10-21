from django.db import models
from django.contrib.auth.models import User
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from django.utils import timezone


class Settings_forms(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
    is_lastname = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_phone = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_city = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_import = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_origin = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_code = models.BooleanField(default=True, db_index=False,blank=False,null=True)
    is_guest = models.BooleanField(default=True, db_index=False,blank=False,null=True)
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
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
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
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
    time = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    cash = models.PositiveIntegerField(blank=True, null=True, db_index=True)

    class Meta:
        managed = True
        db_table = 'Payments'

    def __str__(self):
        return str(self.owner_user)


class Views(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)

    class Meta:
        managed = True
        db_table = 'views'

    def __str__(self):
        return str(self.owner_user)

































"""class User_App(models.Model):
    owner = models.ManyToManyField(User, through='Reservation')
    username = models.CharField(max_length=40, unique=False, null=False, db_index=True)
    password = models.CharField(max_length=255, unique=False, null=False, db_index=True)
    birthdate = models.CharField(max_length=40, unique=False, null=False, db_index=True)
    #date
    #date = models.DateTimeField(default=timezone.now)
    lastname = models.CharField(max_length=255, unique=False, null=False, db_index=True)
    email = models.CharField(max_length=255, unique=False, null=False, db_index=True)
    nif = models.CharField(max_length=255, unique=False, null=False, db_index=True)
    phone = models.IntegerField(max_length=40, unique=False, null=False, db_index=True)
    country = models.CharField(max_length=255, unique=False, null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'users'


class Reservation(models.Model):
    id_reseve = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    owner_id = models.ForeignKey(User, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User_App, on_delete=models.PROTECT)
    flat_id = models.IntegerField(max_length=40, unique=False, null=False, db_index=True)
    #EN INGLES
    #fecha_inicio = models.CharField(max_length=255, default=True, db_index=True)
    #fecha_fin = models.CharField(max_length=255, default=True, db_index=True)

    #guest

    #huespedes_reserva = models.IntegerField(max_length=40, unique=False, null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'reservation'"""
