# HomeBox
<p>Smart home server on Django.</p>
<p>Collects and displays data from sensors, weather forecast service (OpenWeather).</p>
<p>You can connect your devices (such as Arduino).</p>
<b>! the project is under development !</b>

# Server install:
- <code>sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt autoremove -y</code>
- install docker https://docs.docker.com/engine/install/debian/ for Raspbian!
- install PostgreSQL locally:
  -  <code>sudo apt install postgresql postgresql-contrib -y</code>
  - config DB: <code>sudo -u postgres psql</code>
- (*or optional) create and run PostgreSQL container with auto restart:
  - <code>docker run -d --name rpi-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres --restart always postgres:latest</code>
  - config DB: <code>docker exec -it rpi-postgres psql -U postgres</code>
- create and run Rabbitmq (with manager) container <code>docker run -d --hostname localhost --name some-rabbit -p 5672:5672 -p 15672:15672 --restart always rabbitmq:3-management</code>
- install some packages:
  - <code>sudo apt-get install -y nginx python3-dev libpq-dev virtualenv supervisor</code>
  - <code>sudo python3 -m pip install --upgrade setuptools pip wheel pip-tools</code>
- clone repository <code>git clone https://github.com/Valentin-Golyonko/HomeBox.git</code> and <code>cd HomeBox/</code>
- add permissions to .sh scripts:
  - <code>chmod +x config/gunicorn/start_gunicorn.sh</code>
  - <code>chmod +x config/celery_sh/celery.sh</code>
- create config/settings/local.py with postgres and celery config
- create and activate virtual environment:
  - <code>python3 -m venv venv</code>
  - <code>. venv/bin/activate</code>
- inside venv:
  - <code>pip install --upgrade setuptools pip wheel pip-tools</code>
  - generate requirements.txt: <code>pip-compile</code>
  - install dependencies: <code>pip-sync</code> or <code>pip install -r requirements.txt</code>
  - <code>python manage.py migrate</code>
  - <code>python manage.py collectstatic --no-input</code>
  - <code>python manage.py createsuperuser</code>
  - check celery:
    - <code>celery multi start worker -A config -c4 -B -l info --logfile=./logs/%n.log --pidfile=./logs/%n.pid</code>
    - logs in HomeBox/logs/worker.log
    - and result backend on http://127.0.0.1:8000/api/core/celery_test_run/
  - check django:
    - <code>python manage.py runserver 0:8000</code>
    - http://127.0.0.1:8000
  - if all good - stop django server (ctrl+c), celery (kill -HUP $pid)
  - check gunicorn:
    - <code>. ./config/gunicorn/start_gunicorn.sh</code>
    - if you see django on http://127.0.0.1:8001, it's mean that gunicorn is ok
- edit nginx config:
  - <code>sudo nano /etc/nginx/sites-enabled/default</code>
  - copy your config from 'config/nginx/nginx.conf'
- check if it's ok <code>sudo nginx -t</code>
- and <code>sudo service nginx restart</code>
- you may run start_gunicorn.sh and see django on 'server_ip' (not port needed)
- setup supervisor config for gunicorn and celery:
  - <code>sudo nano /etc/supervisor/conf.d/homebox.conf</code>
  - <code>sudo nano /etc/supervisor/conf.d/celeryd.conf</code>
- <code>sudo service supervisor restart</code>
- supervisor logs is here <code>sudo nano /var/log/supervisor/supervisord.log</code>
- celery result backend check on http://'server_ip'/api/core/celery_test_run/

# Sensors install:
- check I2C BME280 sensor - <code>i2cdetect -y 1</code>
- 
