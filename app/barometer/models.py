from django.db import models


class Barometer(models.Model):
    temperature_c = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    pressure_hpa = models.DecimalField(max_digits=6, decimal_places=2)
    device = models.ForeignKey('core.Device', on_delete=models.CASCADE, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Barometer'
        verbose_name_plural = 'Barometer'
        ordering = ('device', 'time_created')
