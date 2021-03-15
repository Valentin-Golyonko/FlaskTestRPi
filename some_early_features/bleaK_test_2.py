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


class BLEData:

    def __init__(self):
        self.data_ = ''

    def notification_handler(self, sender: int, data: bytearray) -> None:
        """Simple notification handler which prints the data received."""
        data_chunk = data.decode('utf-8')
        self.data_ += data_chunk
        print(f"sender: {sender}, data_chunk: {data_chunk}")


def ble_led_strip() -> Device:
    return Device.objects.filter(
        device_type=Choices.DEVICE_TYPE_LED_STRIP,
        sub_type=Choices.DEVICE_SUB_TYPE_RGB_STRIP_WITH_ALARM,
        address_type=Choices.DEVICE_ADDRESS_TYPE_BLUETOOTH,
        mac_address__isnull=False,
    ).first()


async def connect_send_get_ble_data(device_mac_address: str,
                                    json_data: dict,
                                    send_data: bool = True,
                                    get_data: bool = True) -> None:
    async with BleakClient(device_mac_address) as client:
        device = await client.is_connected()
        logger.info(f"Connected to {device}")

        if send_data:
            # send data to ble device
            await client.write_gatt_char(
                ble_led_strip_obj.bluetooth_uuid_tx,
                bytearray(json.dumps(json_data).encode('utf-8'))
            )

        if get_data:
            # get data from ble device
            ble_data_cls = BLEData()
            await client.start_notify(
                ble_led_strip_obj.bluetooth_uuid_rx,
                ble_data_cls.notification_handler
            )
            await asyncio.sleep(5.0)
            await client.stop_notify(ble_led_strip_obj.bluetooth_uuid_rx)

            print(f"summary data: {json.loads(ble_data_cls.data_)}")


if __name__ == '__main__':

    ble_led_strip_obj = ble_led_strip()

    if ble_led_strip_obj:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(connect_send_get_ble_data(
            ble_led_strip_obj.mac_address,
            {"hello": "world"}
        ))
