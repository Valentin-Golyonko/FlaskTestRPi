# Generated by Django 3.1.7 on 2021-02-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owm_forecast', '0004_forecast_latest_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='latest_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
