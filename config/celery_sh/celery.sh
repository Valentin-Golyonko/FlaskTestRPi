#!/bin/bash
source /home/pi/HomeBox/venv/bin/activate
exec "celery worker -A config -c4 -B -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid"