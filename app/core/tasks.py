import logging
from random import randint

from config.celery import app

logger = logging.getLogger(__name__)


@app.task(name='app.core.tasks.task_celery_test_run', ignore_result=False)
def task_celery_test_run() -> int:
    some_int = randint(0, 10)
    logger.info(f"task_celery_test_run(): some_int: {some_int}.")
    return some_int
