"""
Adafruit BME280 Library - https://circuitpython.readthedocs.io/projects/bme280/en/latest/

RPi commands:
pip3 install adafruit-circuitpython-bme280
pip3 install --upgrade adafruit_blinka
i2cdetect -y 1
"""
from datetime import datetime
import sqlite3
from time import sleep

from .color_log.log_color import log_verbose, log_error, log_info


def bme280_date(delta_time=5):
    log_verbose("bme280_date()")
    try:
        import adafruit_bme280
        import board
        import busio
        from micropython import const

        # Create library object using our Bus I2C port
        i2c = busio.I2C(board.SCL, board.SDA)
        address = adafruit_bme280._BME280_ADDRESS = const(0x76)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=address)

        # OR create library object using our Bus SPI port
        # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        # bme_cs = digitalio.DigitalInOut(board.D10)
        # bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

        # change this to match the location's pressure (hPa) at sea level
        bme280.sea_level_pressure = 1013.25

        while True:
            temperature = "%.2f" % bme280.temperature
            humidity = "%.2f" % bme280.humidity
            pressure = "%.2f" % bme280.pressure
            # altitude = "%.2f" % bme280.altitude
            # log_info("\ttemp %s, hum %s, pres %s, alt %s" % (temperature, humidity, pressure, altitude))
            yield temperature, humidity, pressure
            sleep(delta_time)

    except Exception as ex:
        log_error("\tadafruit_bme280: \n%s" % ex)


def update_bme280_db_table():
    log_verbose("update_bme280_db_table()")

    bme280 = bme280_date(600)  # timer = 10 min
    try:
        while True:
            t, h, p = next(bme280)
            db = sqlite3.connect("data/flask_test.sqlite")
            # db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO bme280 (temperature, humidity, pressure, created)'
                ' VALUES (?, ?, ?, ?)',
                (t, h, p, datetime.now(),)
            )
            db.commit()
            db.close()
            if t and h and p:
                log_info("\tupdate_bme280_db_table - OK")
            else:
                log_error("\tError with bme280 values")
    except Exception as ex:
        log_error("\tEx. in - update_bme280_db_table: \n%s" % ex)


if __name__ == '__main__':
    _bme280 = bme280_date(2)
    while True:
        next(_bme280)
    # update_db()
