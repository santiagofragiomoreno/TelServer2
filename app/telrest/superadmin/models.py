from django.contrib.auth.models import User
from django.db import models

# tablas creadas nuevas
"""from telapi.models import Flat


class OwnersData(models.Model):
    person_type = models.BooleanField(default=True, db_index=True)  # true si es persona, false si es empresa
    name = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si persona
    last_name = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si persona
    dni = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si persona
    denomination = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si empresa
    manager = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si empresa
    cif = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # si empresa
    email = models.EmailField(blank=True, db_index=True)
    owner_user = models.ForeignKey(User, models.DO_NOTHING)  # fk de auth_user
    address = models.CharField(max_length=1024, unique=False, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    door = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    city = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'owners_data'


class FlatData(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, db_index=True)
    address = models.CharField(max_length=1024, unique=False, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    door = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    city = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    # añado sobre el flat:
    guests = models.PositiveIntegerField(blank=True, null=True, db_index=True)  # huespedes
    rooms = models.PositiveIntegerField(blank=True, null=True, db_index=True)  # habitaciones
    baths = models.PositiveIntegerField(blank=True, null=True, db_index=True)  # baños
    reference = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # referencia catastral
    meters = models.PositiveIntegerField(blank=True, null=True, db_index=True)  # metros del piso
    owners_data = models.ForeignKey(OwnersData, models.DO_NOTHING, db_index=True)  # fk de owners_data

    class Meta:
        managed = True
        db_table = 'flat_data'
        """
