import logging
from random import randint

from celery import shared_task
from celery.schedules import crontab

from app.core.scripts.berrez_melody import alarm_buzzer_melody
from config.celery import app

logger = logging.getLogger(__name__)


@app.task
def task_morning_alarm():
    alarm_buzzer_melody()


@shared_task
def task_celery_test_run() -> int:
    some_int = randint(0, 10)
    logger.info(f"task_celery_test_run(): some_int: {some_int}.")
    return some_int


app.conf.beat_schedule = {
    'morning-alarm-1': {
        'task': 'app.core.tasks.task_morning_alarm',
        'schedule': crontab(hour=9, minute=0),
    },
}

app.conf.beat_schedule = {
    'morning-alarm-2': {
        'task': 'app.core.tasks.task_morning_alarm',
        'schedule': crontab(hour=9, minute=10),
    },
}

app.conf.beat_schedule = {
    'morning-alarm-3': {
        'task': 'app.core.tasks.task_morning_alarm',
        'schedule': crontab(hour=9, minute=20),
    },
}
