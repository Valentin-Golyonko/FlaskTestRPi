# Generated by Django 3.2.4 on 2021-06-30 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_alive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
