# Generated by Django 3.1.4 on 2020-12-19 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owm_forecast', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecast',
            name='main_source',
            field=models.BooleanField(default=False),
        ),
    ]
