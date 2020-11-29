import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('HomeBox')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery multi start worker -A config -c2 -B -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid
# kill -HUP $pid
