# Generated by Django 3.0.7 on 2020-10-26 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='birthdate',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='settings_forms',
            name='is_birthdate',
        ),
    ]
