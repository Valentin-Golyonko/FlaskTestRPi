#!/bin/bash
source /home/pi/HomeBox/venv/bin/activate
python manage.py migrate
python manage.py collectstatic --no-input
rm logs/*.pid
sleep 5
exec gunicorn -c "/home/pi/HomeBox/config/gunicorn/gunicorn_config.py" config.wsgi