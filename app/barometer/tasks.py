import logging

from app.barometer.scripts.barometer_sensor import request_barometer_data
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(name='app.barometer.tasks.task_request_barometer_data', ignore_result=True)
def task_request_barometer_data() -> None:
    try:
        request_barometer_data()
    except Exception as ex:
        logger.error(f"task_request_barometer_data(): {ex}")
