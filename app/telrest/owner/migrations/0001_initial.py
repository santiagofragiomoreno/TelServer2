# Generated by Django 3.0.7 on 2020-10-21 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'views',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Settings_forms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_lastname', models.BooleanField(default=True, null=True)),
                ('is_phone', models.BooleanField(default=True, null=True)),
                ('is_city', models.BooleanField(default=True, null=True)),
                ('is_import', models.BooleanField(default=True, null=True)),
                ('is_origin', models.BooleanField(default=True, null=True)),
                ('is_code', models.BooleanField(default=True, null=True)),
                ('is_guest', models.BooleanField(default=True, null=True)),
                ('is_cancelation', models.BooleanField(default=True, null=True)),
                ('is_observation', models.BooleanField(default=True, null=True)),
                ('is_pay', models.BooleanField(default=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'settings_forms',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Settings_alerts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_temperature', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('min_temperature', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('start_time', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('end_time', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('max_capacity', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('listening_time', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'settings_alerts',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_time', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('time_price', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'payments',
                'managed': True,
            },
        ),
    ]
