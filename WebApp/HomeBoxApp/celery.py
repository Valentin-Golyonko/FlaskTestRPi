import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

from sensors.tasks import print_hello

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HomeBoxApp.settings')

app = Celery('HomeBoxApp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(),  # minute='*/10'
        print_hello.s('Sensors!'),
    )
