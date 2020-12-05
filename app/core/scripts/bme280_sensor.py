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

logger = logging.getLogger(__name__)


def get_bme280_data():
    import board
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        address = adafruit_bme280._BME280_ADDRESS = const(0x76)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=address)
        bme280.sea_level_pressure = 1013.25

        logger.info(f"temperature: {bme280.temperature},"
                    f" humidity: {bme280.humidity},"
                    f" pressure: {bme280.pressure}.")
    except Exception as ex:
        logger.exception(f"get_bme280_data(): {ex}.")
