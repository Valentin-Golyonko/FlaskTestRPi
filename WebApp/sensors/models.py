from django.db import models


class Sensors(models.Model):
    name = models.CharField(max_length=20,
                            verbose_name="Sensor name")
    i2c_address = models.PositiveIntegerField(blank=True, null=True,
                                              verbose_name='I2C address')
    ip_address = models.GenericIPAddressField(blank=True, null=True,
                                              verbose_name="IP address")


class SensorData(models.Model):
    sensor = models.ForeignKey(to=Sensors, on_delete=models.CASCADE)

    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)

