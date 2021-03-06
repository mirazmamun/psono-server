# Generated by Django 2.0 on 2018-02-22 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0012_auto_20180122_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether this user has management capabilities or not.', verbose_name='Has managemnet capabilities'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates whether this user is an admin or not.', verbose_name='Admin User'),
        ),
    ]
