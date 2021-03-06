from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstructionUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('grant_id', models.IntegerField()),
                ('access_id', models.IntegerField()),
                ('task_code', models.IntegerField()),
            ],
            options={
                'managed': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, null=True, unique=True)),
                ('address', models.CharField(max_length=1024, null=True)),
                ('floor', models.PositiveIntegerField(blank=True, null=True)),
                ('door', models.CharField(db_index=True, max_length=255, null=True)),
                ('city', models.CharField(db_index=True, max_length=255, null=True)),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True)),
                ('guests', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('rooms', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('baths', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('reference', models.CharField(db_index=True, max_length=255, null=True)),
                ('meters', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254)),
                ('iot_user_id', models.PositiveIntegerField(blank=True, null=True)),
                ('access_code', models.CharField(db_index=True, max_length=255, null=True, unique=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'grant',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('code', models.PositiveSmallIntegerField(unique=True)),
            ],
            options={
                'db_table': 'task',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_type_id', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('value', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('iot_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iot_user_id', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ownership',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OwnersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_type', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(db_index=True, max_length=255, null=True)),
                ('last_name', models.CharField(db_index=True, max_length=255, null=True)),
                ('dni', models.CharField(db_index=True, max_length=255, null=True)),
                ('denomination', models.CharField(db_index=True, max_length=255, null=True)),
                ('manager', models.CharField(db_index=True, max_length=255, null=True)),
                ('cif', models.CharField(db_index=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254)),
                ('address', models.CharField(max_length=1024, null=True)),
                ('floor', models.PositiveIntegerField(blank=True, null=True)),
                ('door', models.CharField(db_index=True, max_length=255, null=True)),
                ('city', models.CharField(db_index=True, max_length=255, null=True)),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True)),
                ('phone', models.PositiveIntegerField(blank=True, null=True)),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'owners_data',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('recieved', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('recieved_date', models.DateTimeField(blank=True, null=True)),
                ('grant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.Grant')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'instruction',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FlatOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iot_user_id', models.PositiveIntegerField(blank=True, db_index=True, null=True)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.Flat')),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='flat',
            name='owners_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.OwnersData'),
        ),
        migrations.CreateModel(
            name='Flat_Owner_Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_access', models.CharField(db_index=True, max_length=255)),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.Flat')),
            ],
            options={
                'db_table': 'flat_owner_access',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=255, unique=True)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('grant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telapi.Grant')),
            ],
        ),
    ]
