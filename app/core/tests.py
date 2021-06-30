from django.test import TestCase

from app.core.core_scripts.choices import Choices
from app.core.models import Device


class DeviceTest(TestCase):
    def setUp(self) -> None:
        pass

    @staticmethod
    def test_device_create_1():
        device_obj = Device(
            title='some device',
            device_type=Choices.DEVICE_TYPE_BAROMETER,
            sub_type=Choices.DEVICE_SUB_TYPE_BME280,
            address_type=Choices.DEVICE_ADDRESS_TYPE_I2C,
            i2c_address='0x77',
        )
        device_obj.save()

    @staticmethod
    def test_device_create_2():
        device_obj = Device(
            title='some device',
            device_type=Choices.DEVICE_TYPE_BAROMETER,
            sub_type=Choices.DEVICE_SUB_TYPE_BME280,
            address_type=Choices.DEVICE_ADDRESS_TYPE_I2C,
            ip_address='0.0.0.0',
        )
        device_obj.save()
