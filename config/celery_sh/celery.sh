#!/bin/bash
source /home/pi/HomeBox/venv/bin/activate
exec celery multi start worker -A config.celery:app -c4 -B -l info