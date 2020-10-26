from django.db import models
from django.contrib.auth.models import User

#from superadmin.models import OwnersData


class Instruction(models.Model):
    task = models.ForeignKey('Task', models.DO_NOTHING)
    issued_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    recieved = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    recieved_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
    grant = models.ForeignKey('Grant', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'instruction'

    def __str__(self):
        return self.user.username + ' - '+str(self.task.name) + " - " + str(self.issued_date)


class Task(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    code = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        managed = True
        db_table = 'task'

    def __str__(self):
        return str(self.code) + " - " + self.name


class Ownership(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
    iot_user_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ownership'


class Grant(models.Model):
    email = models.EmailField(blank=True, db_index=True)
    owner_user = models.ForeignKey(User, models.DO_NOTHING)
    iot_user_id = models.PositiveIntegerField(blank=True, null=True)
    access_code = models.CharField(max_length=255, unique=True, null=True, db_index=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'grant'


class Access(models.Model):
    grant = models.ForeignKey('Grant', models.DO_NOTHING)
    token = models.CharField(max_length=255, unique=True, null=False, db_index=True)
    active = models.BooleanField(default=True, db_index=True)


class InstructionUser(User):
    grant_id = models.IntegerField()
    access_id = models.IntegerField()
    task_code = models.IntegerField()

    class Meta:
        managed = False


class SensorData(models.Model):
    iot_user = models.ForeignKey(User, models.DO_NOTHING)
    sensor_type_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    value = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, db_index=True)


class SensorType(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, db_index=True)


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


class Flat(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, db_index=True)
    address = models.CharField(max_length=1024, unique=False, null=True)
    floor = models.PositiveIntegerField(blank=True, null=True)
    door = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    city = models.CharField(max_length=255, unique=False, null=True, db_index=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True)
    #  nuevos campos de pisos
    guests = models.PositiveIntegerField(blank=True, unique=False, null=True, db_index=True)  # huespedes
    rooms = models.PositiveIntegerField(blank=True, unique=False, null=True, db_index=True)  # habitaciones
    baths = models.PositiveIntegerField(blank=True, unique=False, null=True, db_index=True)  # baños
    reference = models.CharField(max_length=255, unique=False, null=True, db_index=True)  # referencia catastral
    meters = models.PositiveIntegerField(blank=True, unique=False, null=True, db_index=True)  # metros del piso
    owners_data = models.ForeignKey('OwnersData', models.DO_NOTHING, db_index=True)  # fk de owners_data


class FlatOwner(models.Model):
    owner_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True)
    flat = models.ForeignKey(Flat, models.DO_NOTHING, db_index=True)
    iot_user_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)


class Flat_Owner_Access(models.Model):
    auth_user = models.ForeignKey(User, models.DO_NOTHING, db_index=True, null=False,)
    flat = models.ForeignKey(Flat, models.DO_NOTHING, db_index=True, null=False,)
    date_access=models.CharField(max_length=255, null=False, db_index=True)

    class Meta:
        managed = True
        db_table = 'flat_owner_access'


