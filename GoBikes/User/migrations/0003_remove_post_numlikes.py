# Generated by Django 4.0.3 on 2022-04-08 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_user_is_admin_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='numLikes',
        ),
    ]