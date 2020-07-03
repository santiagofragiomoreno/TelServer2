from django.db import models


class Instruction(models.Model):
    task = models.ForeignKey('Task', models.DO_NOTHING)
    issued_date = models.DateTimeField(blank=True, null=True)
    recieved_date = models.DateTimeField(blank=True, null=True)
    recieved = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instruction'


class Task(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    code = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'task'
