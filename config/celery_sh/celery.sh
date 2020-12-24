#!/bin/bash
source /home/pi/HomeBox/venv/bin/activate
celery -A config.celery:app worker -c4 -B -l warning --logfile=./logs/%n.log --pidfile=./logs/%n.pid