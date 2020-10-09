from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# TODO es necesario crear un nuevo modelo para BBDD que se llame acceso que permita relacionar a los usuarios con los owner bajo un acceso
# la tabla debera llevar id de usuario, id del owner (N:M) y los campos deben ser fecha, piso escogido para la fecha o en su defecto una que sea accesos


class User_App(models.Model):
    owner = models.ManyToManyField(User, through='Reservation')
    username = models.CharField(
        max_length=40, unique=False, null=False, db_index=True)
    password = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)
    birthdate = models.CharField(
        max_length=40, unique=False, null=False, db_index=True)
    date = models.DateTimeField(default=timezone.now)
    lastname = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)
    email = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)
    nif = models.CharField(max_length=255, unique=False,
                           null=False, db_index=True)
    phone = models.IntegerField(
        max_length=40, unique=False, null=False, db_index=True)
    city = models.CharField(max_length=255, unique=False,
                            null=False, db_index=True)
    country = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)
    cp = models.CharField(max_length=255, unique=False,
                          null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'users'


class Rols(models.Model):
    id_rol = models.IntegerField(
        max_length=40, unique=False, null=False, db_index=True)
    rol = models.CharField(max_length=40, unique=False,
                           null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'rols'


class User_Rols(models.Model):
    id_user = models.ForeignKey(User, models.DO_NOTHING)
    id_rol = models.ForeignKey(Rols, models.DO_NOTHING)
    name_userols = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)
    id_userol = models.CharField(
        max_length=255, unique=False, null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'user_rols'


class Reservation(models.Model):
    user_id = models.ForeignKey(User_App, on_delete=models.PROTECT)
    owner_id = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_inicio = models.CharField(
        max_length=255, default=True, db_index=True)
    fecha_fin = models.CharField(max_length=255, default=True, db_index=True)
    huespedes_reserva = models.IntegerField(
        max_length=40, unique=False, null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'reservation'
