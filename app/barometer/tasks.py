from celery.schedules import crontab

from app.barometer.scripts.barometer_sensor import get_barometer_data
from config.celery import app


@app.task
def task_get_barometer_data() -> None:
    get_barometer_data()


app.conf.beat_schedule = {
    'get-barometer-data': {
        'task': 'app.barometer.tasks.task_get_barometer_data',
        'schedule': crontab(minute='*/10'),
    },
}
