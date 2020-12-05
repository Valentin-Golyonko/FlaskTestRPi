#!/bin/bash
source /home/pi/HomeBox/venv/bin/activate
exec gunicorn -c "/home/pi/HomeBox/config/gunicorn/gunicorn_config.py" config.wsgi