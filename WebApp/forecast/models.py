from django.db import models


class City(models.Model):
    city_id = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=10)
    lng = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
