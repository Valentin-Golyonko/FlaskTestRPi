import logging
from typing import Tuple

from asgiref.sync import sync_to_async

from app.core.ble_control.bleak_client import BLEControl
from app.rgb_control.rgb_control_scripts.get_rgb_divice import GetRGBDevice

logger = logging.getLogger(__name__)


class SetLEDStripColor:

    @staticmethod
    async def set_rgb_strip_color(validated_data: dict) -> Tuple[bool, dict]:
        ble_led_strip_alarm_obj = await sync_to_async(GetRGBDevice.ble_led_strip_alarm, thread_sensitive=True)()
        if ble_led_strip_alarm_obj is None:
            logger.error(f"set_rgb_strip_color(): ble_led_strip_obj is None")
            return False, {'detail': "ble_led_strip_obj is None"}

        data_to_send = {}
        alpha = validated_data.pop('alpha')
        for key, value in validated_data.items():
            data_to_send[key] = int(value * alpha)

        try:
            await BLEControl.connect_send_get_ble_data(ble_led_strip_alarm_obj, data_to_send)
        except Exception as ex:
            logger.exception(f"set_rgb_strip_color(): {ex}")
            return False, {'detail': "some error"}
        else:
            return True, {}
