"""
python manage.py runscript app.core.ble_control.bleak_client

rpi commands:
    rfkill list
    rfkill unblock all
    bluetoothctl power on
    sudo bluetoothctl
    agent on
    default-agent
    scan on
    pair XX:XX:XX:XX:XX:XX
    connect XX:XX:XX:XX:XX:XX
"""
import asyncio
import json
import logging
import os
import sys
from asyncio import sleep

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

from app.rgb_control.rgb_control_scripts.get_rgb_divice import GetRGBDevice
from app.core.models import Device

logger = logging.getLogger(__name__)


class BLEControl:

    @classmethod
    def ping_ble_led_strip_alarm(cls) -> None:
        ble_led_strip_alarm_obj = GetRGBDevice.ble_led_strip_alarm()
        if ble_led_strip_alarm_obj is None:
            logger.error(f"ping_ble_led_strip(): ble_led_strip_obj is None")
            return None

        try:
            loop = asyncio.get_event_loop()
            device_response = loop.run_until_complete(
                cls.connect_send_get_ble_data(
                    ble_led_strip_alarm_obj,
                    {"ping": "ping"}
                )
            )
        except Exception as ex:
            logger.exception(f"ping_ble_led_strip_alarm(): {ex}")
            is_alive_ = False
        else:
            pong = device_response.get('ping')
            if pong != 'pong':
                is_alive_ = False
                logger.error(f"ping_ble_led_strip_alarm(): device_response != 'pong';"
                             f" {device_response}")
            else:
                is_alive_ = True
                logger.info(f"ping_ble_led_strip_alarm(): device_response: {pong}")

        ble_led_strip_alarm_obj.is_alive = is_alive_
        ble_led_strip_alarm_obj.save()

    @staticmethod
    async def connect_send_get_ble_data(ble_device_obj: Device,
                                        json_data: dict,
                                        send_data: bool = True,
                                        get_data: bool = True) -> dict:
        device_response = {}
        logger.info(f"connect_send_get_ble_data(): info;"
                    f" {ble_device_obj.id = }, {json_data = }")

        try:
            async with BleakClient(ble_device_obj.mac_address) as client:
                logger.info(f"Connected: {client.is_connected()}")

                if send_data:
                    # send data to ble device
                    for key, value in json_data.items():
                        await client.write_gatt_char(
                            ble_device_obj.bluetooth_uuid_tx,
                            bytearray(json.dumps({key: value}).encode('utf-8'))
                        )
                        await sleep(.1)  # 100ms

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
