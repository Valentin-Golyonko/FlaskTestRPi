#!/bin/bash
mkdir logs
rm logs/*.pid
python manage.py migrate
python manage.py collectstatic --no-input
sleep 5
celery multi start worker -A config -c4 -B -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid
sleep 5
python manage.py runserver 192.168.0.102:8000
