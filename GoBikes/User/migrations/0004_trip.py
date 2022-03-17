# Generated by Django 4.0.3 on 2022-03-17 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_rename_location_user_currentlocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
                ('location', models.ManyToManyField(to='User.location')),
            ],
        ),
    ]