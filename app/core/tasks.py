import logging

from celery import shared_task

from config.celery import app

logger = logging.getLogger(__name__)


# celery multi start worker -A config -c2 beat -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid
# celery -A config beat -l INFO

@app.task
def morning_alarm(**kwargs) -> None:
    logger.info("time to wake up!")

    logger.info(f"{kwargs.get('hello')}")

    print(f"{kwargs.get('hello')}")

    return None


@shared_task
def task_2(**kwargs) -> None:
    logger.info("task_2()")

    logger.info(f"{kwargs.get('hello')}")

    print(f"{kwargs.get('hello')}")

    return None
