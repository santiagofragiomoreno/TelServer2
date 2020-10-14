# Generated by Django 3.0.7 on 2020-10-09 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id_reseve', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('flat_id', models.IntegerField(db_index=True, max_length=40)),
                ('fecha_inicio', models.CharField(db_index=True, default=True, max_length=255)),
                ('fecha_fin', models.CharField(db_index=True, default=True, max_length=255)),
                ('huespedes_reserva', models.IntegerField(db_index=True, max_length=40)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reservation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Rols',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_rol', models.IntegerField(db_index=True, max_length=40)),
                ('rol', models.CharField(db_index=True, max_length=40)),
            ],
            options={
                'db_table': 'rols',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User_Rols',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_rol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.Rols')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_rols',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='User_App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=40)),
                ('password', models.CharField(db_index=True, max_length=255)),
                ('birthdate', models.CharField(db_index=True, max_length=40)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('lastname', models.CharField(db_index=True, max_length=255)),
                ('email', models.CharField(db_index=True, max_length=255)),
                ('nif', models.CharField(db_index=True, max_length=255)),
                ('phone', models.IntegerField(db_index=True, max_length=40)),
                ('city', models.CharField(db_index=True, max_length=255)),
                ('country', models.CharField(db_index=True, max_length=255)),
                ('cp', models.CharField(db_index=True, max_length=255)),
                ('owner', models.ManyToManyField(through='login.Reservation', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'users',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='login.User_App'),
        ),
    ]