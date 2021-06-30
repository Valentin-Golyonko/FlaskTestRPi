from django.db import models

from app.core.core_scripts.choices import Choices


class Forecast(models.Model):
    title = models.CharField(max_length=20)
    api_key = models.CharField(max_length=100)
    city = models.CharField(max_length=20, help_text='Minsk, Belarus')
    units = models.PositiveSmallIntegerField(
        choices=Choices.FORECAST_UNITS_CHOICES, default=Choices.FORECAST_UNITS_METRIC,
    )
    main_source = models.BooleanField(default=False)

    geo_coord = models.JSONField(blank=True, null=True)
    current_weather_data = models.JSONField(blank=True, null=True)
    current_air_pollution_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.title
