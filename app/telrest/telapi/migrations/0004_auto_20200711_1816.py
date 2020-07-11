# Generated by Django 3.0.7 on 2020-07-11 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('telapi', '0003_auto_20200708_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grant',
            name='client_user',
        ),
        migrations.AddField(
            model_name='grant',
            name='access_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='grant',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='grant',
            name='owner_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
