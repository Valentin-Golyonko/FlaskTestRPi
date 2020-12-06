from celery.schedules import crontab

from app.barometer.scripts.bme280_sensor import get_bme280_data
from config.celery import app


@app.task
def task_get_bme280_data() -> None:
    get_bme280_data()


app.conf.beat_schedule = {
    'get-bme280-data': {
        'task': 'app.barometer.tasks.task_get_bme280_data',
        'schedule': crontab(minute='*/10'),
    },
}
