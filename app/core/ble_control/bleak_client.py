"""
python manage.py runscript app.core.ble_control.bleak_client
"""
import asyncio
import json
import logging
import os
import sys

import django
from bleak import BleakClient

""" for local usage -> """
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
""" <- for local usage """

from app.core.choices import Choices
from app.core.models import Device

logger = logging.getLogger(__name__)


class BLEControl:

    @staticmethod
    def ble_led_strip_alarm() -> Device:
        return Device.objects.filter(
            device_type=Choices.DEVICE_TYPE_LED_STRIP,
            sub_type=Choices.DEVICE_SUB_TYPE_RGB_STRIP_WITH_ALARM,
            address_type=Choices.DEVICE_ADDRESS_TYPE_BLUETOOTH,
            mac_address__isnull=False,
        ).first()

    @classmethod
    def ping_ble_led_strip_alarm(cls) -> None:
        ble_led_strip_alarm_obj = cls.ble_led_strip_alarm()
        if ble_led_strip_alarm_obj is None:
            logger.error(f"ping_ble_led_strip(): ble_led_strip_obj is None")
            return None

        try:
            loop = asyncio.get_event_loop()
            device_response = loop.run_until_complete(cls.connect_send_get_ble_data(
                ble_led_strip_alarm_obj,
                {"ping": "ping"}
            ))
            loop.close()
        except Exception as ex:
            logger.exception(f"ping_ble_led_strip_alarm(): {ex}")
        else:
            pong = device_response.get('ping')
            if pong != 'pong':
                logger.error(f"ping_ble_led_strip_alarm(): device_response != 'pong', {device_response}")
            logger.info(f"ping_ble_led_strip_alarm(): device_response: {pong}")

    @staticmethod
    async def connect_send_get_ble_data(ble_device_obj: Device,
                                        json_data: dict,
                                        send_data: bool = True,
                                        get_data: bool = True) -> dict:
        device_response = {}

        try:
            async with BleakClient(ble_device_obj.mac_address) as client:
                device = await client.is_connected()
                logger.info(f"Connected: {device}")

                if send_data:
                    # send data to ble device
                    await client.write_gatt_char(
                        ble_device_obj.bluetooth_uuid_tx,
                        bytearray(json.dumps(json_data).encode('utf-8'))
                    )

                if get_data:
                    # get data from ble device
                    ble_data_cls = BLEData()
                    await client.start_notify(
                        ble_device_obj.bluetooth_uuid_rx,
                        ble_data_cls.notification_handler
                    )
                    await asyncio.sleep(5.0)
                    await client.stop_notify(ble_device_obj.bluetooth_uuid_rx)

                    device_response = json.loads(ble_data_cls.data_)
        except Exception as ex:
            logger.exception(f"connect_send_get_ble_data(): {ex}")

        logger.debug(f"connect_send_get_ble_data(): device response: {device_response}")
        return device_response


class BLEData:
    def __init__(self):
        self.data_ = ''

    def notification_handler(self, sender: int, data: bytearray) -> None:
        """Simple notification handler which prints the data received."""
        data_chunk = data.decode('utf-8')
        self.data_ += data_chunk
        logger.debug(f"notification_handler(): sender: {sender}, data_chunk: {data_chunk}")


def run():
    BLEControl.ping_ble_led_strip_alarm()


if __name__ == '__main__':
    BLEControl.ping_ble_led_strip_alarm()
