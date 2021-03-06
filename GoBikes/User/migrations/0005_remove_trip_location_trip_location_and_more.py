# Generated by Django 4.0.3 on 2022-03-17 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_trip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='location',
        ),
        migrations.AddField(
            model_name='trip',
            name='location',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='User.location'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='user',
            name='currentLocation',
        ),
        migrations.AddField(
            model_name='user',
            name='currentLocation',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='User.location'),
            preserve_default=False,
        ),
    ]
