# Generated by Django 4.0.3 on 2022-04-10 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_remove_trip_endlat_remove_trip_endlng_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
