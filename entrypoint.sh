#!/bin/bash
mkdir logs
python manage.py migrate
#python manage.py collectstatic --no-input
rm logs/*.pid
sleep 10
celery multi start worker -A config -c4 -B -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid