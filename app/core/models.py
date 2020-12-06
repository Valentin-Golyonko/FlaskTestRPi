from django.db import models

from app.core.choices import Choices


class Device(models.Model):
    title = models.CharField(max_length=50)
    device_type = models.PositiveSmallIntegerField(choices=Choices.DEVICE_TYPE_CHOICES)
    sub_type = models.PositiveSmallIntegerField(choices=Choices.DEVICE_SUB_TYPE_CHOICES)
    address_type = models.PositiveSmallIntegerField(choices=Choices.DEVICE_ADDRESS_TYPE_CHOICES)
    i2c_address = models.CharField(max_length=5, default='', verbose_name='I2C address', null=True)
    ip_address = models.GenericIPAddressField(default='', null=True)

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return self.title
