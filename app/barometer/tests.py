from random import uniform

from django.test import TestCase

from app.barometer.scripts.save_barometer_data import SaveBarometerData


class BarometerTest(TestCase):
    def setUp(self) -> None:
        pass

    @staticmethod
    def test_save_some_data():
        SaveBarometerData.save_barometer_data(
            temperature_c=uniform(-40, 85),
            humidity=uniform(0, 100),
            pressure_hpa=uniform(300, 1100),
        )
