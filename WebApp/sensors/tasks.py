import adafruit_bme280

import busio
from celery import shared_task
from micropython import const


@shared_task
def print_hello(hello_word):
    print(hello_word)
    return -1


@shared_task
def get_bme280_i2c_data(celery_hello):
    print(celery_hello)
    try:
        import board
        i2c = busio.I2C(board.SCL, board.SDA)
        i2c_address = adafruit_bme280._BME280_ADDRESS = const(0x76)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=i2c_address)
        # change this to match the location's pressure (hPa) at sea level
        bme280.sea_level_pressure = 1013.25
    except Exception as ex:
        print(f'Exception in get_bme280_i2c_data:\n{ex}')
    else:
        bme280_data = {"temperature": bme280.temperature,
                       "humidity": bme280.humidity,
                       "pressure": bme280.pressure}

    return 1
