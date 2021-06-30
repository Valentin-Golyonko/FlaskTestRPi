from django.templatetags.tz import localtime

from app.core.core_scripts.choices import Choices
from app.core.models import Device
from app.core.serializers import DeviceSerializer


class GetRGBDevice:

    @staticmethod
    def ble_led_strip_alarm() -> Device:
        return Device.objects.filter(
            device_type=Choices.DEVICE_TYPE_LED_STRIP,
            sub_type=Choices.DEVICE_SUB_TYPE_RGB_STRIP_WITH_ALARM,
            address_type=Choices.DEVICE_ADDRESS_TYPE_BLUETOOTH,
            mac_address__isnull=False,
        ).first()

    @staticmethod
    def device_serialized_data():
        device_obj = GetRGBDevice.ble_led_strip_alarm()
        device_data = DeviceSerializer(device_obj).data
        device_data['last_update'] = localtime(device_obj.last_update)
        return device_data
