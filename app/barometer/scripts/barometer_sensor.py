import logging

import busio
from adafruit_bme280 import basic as adafruit_bme280
from micropython import const

from app.barometer.scripts.save_barometer_data import SaveBarometerData
from app.core.core_scripts.choices import Choices
from app.core.models import Device

logger = logging.getLogger(__name__)


def request_barometer_data() -> None:
    import board

    for device_obj in Device.objects.filter(device_type=Choices.DEVICE_TYPE_BAROMETER):
        try:
            device_module = None

            if device_obj.sub_type == Choices.DEVICE_SUB_TYPE_BME280:
                if device_obj.i2c_address:
                    device_module = adafruit_bme280.Adafruit_BME280_I2C(
                        i2c=busio.I2C(board.SCL, board.SDA),
                        address=const(int(device_obj.i2c_address, 16))
                    )

            if device_obj is not None:
                SaveBarometerData.save_barometer_data(
                    temperature_c=device_module.temperature,
                    humidity=device_module.humidity,
                    pressure_hpa=device_module.pressure,
                    device_obj=device_obj,
                )
        except Exception as ex:
            logger.exception(f"request_barometer_data(): {ex}")
            continue
