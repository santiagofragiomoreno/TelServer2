from django.db import models
from django.contrib.auth.models import User
from telapi.models import Instruction, Task, Ownership, Grant, Access, SensorData, SensorType, FlatOwner, Flat
from django.utils import timezone

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
