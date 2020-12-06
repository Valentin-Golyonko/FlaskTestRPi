"""
Adafruit BME280 Library - https://circuitpython.readthedocs.io/projects/bme280/en/latest/

RPi commands:
pip3 install adafruit-circuitpython-bme280
pip3 install --upgrade adafruit_blinka
i2cdetect -y 1
"""

import logging

import adafruit_bme280

import busio
from micropython import const

from app.barometer.scripts.save_barometer_data import SaveBarometerData

logger = logging.getLogger(__name__)


def get_bme280_data() -> None:
    import board
    try:
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(
            i2c=busio.I2C(board.SCL, board.SDA),
            address=const(0x76)
        )

        SaveBarometerData.save_barometer_data(
            temperature_c=bme280.temperature,
            humidity=bme280.humidity,
            pressure_hpa=bme280.pressure,
        )
    except Exception as ex:
        logger.exception(f"get_bme280_data(): {ex}.")
