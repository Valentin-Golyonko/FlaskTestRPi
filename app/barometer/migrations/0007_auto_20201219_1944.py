# Generated by Django 3.1.4 on 2020-12-19 16:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('barometer', '0006_auto_20201219_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barometer',
            name='time_created',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 19, 16, 44, 55, 137042, tzinfo=utc)),
        ),
    ]
