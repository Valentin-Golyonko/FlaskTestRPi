import os
from time import sleep

from .color_log.log_color import log_verbose, log_error


def measure_rpi_temp(delta_time=2):
    log_verbose("measure_rpi_temp()")
    try:
        while True:
            temp = os.popen("vcgencmd measure_temp").readline()
            temp = str(temp).strip().replace("temp=", "").replace("'C", "")
            if not temp:
                log_error("\tRPi temp = None")
                temp = None
            yield temp
            sleep(delta_time)
    except Exception as ex:
        log_error("RPi measure temp: \n%s" % ex)


if __name__ == "__main__":
    rpi_temp = measure_rpi_temp(2)
    while True:
        next(rpi_temp)
