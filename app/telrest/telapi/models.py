from django.db import models
from django.contrib.auth.models import User


class Instruction(models.Model):
    task = models.ForeignKey('Task', models.DO_NOTHING)
    issued_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    recieved_date = models.DateTimeField(blank=True, null=True)
    recieved = models.PositiveIntegerField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING)

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
