import logging

from app.core.ble_control.bleak_client import BLEControl
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(name='app.rgb_control.tasks.task_update_alive_rgb_strip', ignore_result=True)
def task_update_alive_rgb_strip() -> None:
    try:
        BLEControl.ping_ble_led_strip_alarm()
    except Exception as ex:
        logger.error(f"task_update_alive_rgb_strip(): {ex}")
