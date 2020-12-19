from django.db import models

from app.core.choices import Choices


class Forecast(models.Model):
    title = models.CharField(max_length=20)
    api_key = models.CharField(max_length=100)
    city = models.CharField(max_length=20, help_text='Minsk, Belarus')
    units = models.PositiveSmallIntegerField(
        choices=Choices.FORECAST_UNITS_CHOICES, default=Choices.FORECAST_UNITS_METRIC,
    )
    main_source = models.BooleanField(default=False)

    def __str__(self):
        return self.title
