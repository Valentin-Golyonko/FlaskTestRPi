from sensors.models import Sensors


def upload_sensors_data():
    sensors = Sensors.objects.all()
    for sensor in sensors:
        ip_address, i2c_address = sensor.ip_address, sensor.i2c_address
        if ip_address:
            pass
        elif i2c_address:
            pass
        else:
            pass
