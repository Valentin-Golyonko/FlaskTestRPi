from random import uniform

from django.test import TestCase

from app.barometer.scripts.save_barometer_data import SaveBarometerData
from app.core.core_scripts.choices import Choices
from app.core.models import Device


class BarometerTest(TestCase):
    def setUp(self) -> None:
        self.device_obj = Device.objects.create(
            title='some device',
            device_type=Choices.DEVICE_TYPE_BAROMETER,
            sub_type=Choices.DEVICE_SUB_TYPE_BME280,
            address_type=Choices.DEVICE_ADDRESS_TYPE_I2C,
            i2c_address='0x77',
        )

    def test_save_some_data(self):
        SaveBarometerData.save_barometer_data(
            temperature_c=uniform(-40, 85),
            humidity=uniform(0, 100),
            pressure_hpa=uniform(300, 1100),
            device_obj=self.device_obj,
        )
