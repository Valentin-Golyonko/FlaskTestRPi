"""
Weather API:
    https://openweathermap.org/api
"""
import datetime
import json
import sqlite3
import urllib.request
from time import sleep

from flask import (
    Blueprint, render_template, request)

import api_keys.keys as key
from color_log.log_color import *
from db import get_db, close_db

bp = Blueprint('weather', __name__)


@bp.route('/weather', methods=('GET', 'POST'))
def index():
    log_verbose("weather: index()")
    data = []

    if request.method == 'POST':
        log_info("\tPOST")
        city = request.form['city']
        log_warning("\tcity: %s" % city)
        if city:
            city = str(city).split()
            log_info("\tcity: %s" % city)
            city_id = open_city_json(city[0], city[1])
            log_info("\tcity_id: %s" % city_id)

    try:
        cur = get_db().cursor()
        owm_db_data = cur.execute(
            'SELECT *'
            ' FROM owm'
            ' ORDER BY time_unix DESC LIMIT 1'
        ).fetchall()
        close_db()
        log_info("\tOpen owm table - OK")

        data = [i for i in owm_db_data[0]]

        dt = datetime.datetime.utcfromtimestamp(data[11])  # convert from unix time
        log_info("\tlast owm time: " + str(dt))  # test print
        data[11] = str(dt)

    except sqlite3.DatabaseError as err:
        log_error("\tEx. in - weather: index(): \n%s" % err)
    finally:
        close_db()

    return render_template('weather.html', owm_db_data=data)
    # return redirect(url_for('sensors.index'))


def update_owm_db_table():
    log_verbose("update_owm_db_table()")
    _owm = owm(600)  # timer = 10 min
    try:
        while True:
            owm_data = next(_owm)
            db = sqlite3.connect("data/flask_test.sqlite")
            # db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO owm (weather_id, description,"
                           " icon, temp, pressure, humidity, temp_min,"
                           " temp_max, wind_speed, wind_deg, wind_gust, time_unix)"
                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", owm_data)

            db.commit()
            db.close()
            log_info("\tupdate_owm_db_table - OK")
    except Exception as ex:
        log_error("\tEx. in - update_owm_db_table: \n%s" % ex)
        db.close()


def open_city_json(input_city, country_code):
    log_verbose("open_city_json()")

    with open("data/city.list.json", encoding="utf8") as f_city:
        data_city = json.load(f_city)
    log_info("\topened")

    city_id = 0
    for city in data_city:
        if city["name"] == input_city and city["country"] == country_code:
            city_id = city["id"]
            log_info("\tcity: %s, %s, id: %d" % (str(city["name"]), str(city["country"]), city_id))
            break

    if city_id == 0:
        log_error("\tNo such city in the base. \nPlease, check your input or select nearest city to yours")

    return city_id


def owm(delta_time=600):
    log_verbose("owm()")

    id_city = open_city_json("Minsk", "BY")
    try:
        while True:
            owm_output = []
            owm_call = "http://api.openweathermap.org/data/2.5/weather?id=" + \
                       str(id_city) + "&units=metric&APPID=" + str(key.owm_api_key)

            owm_data = urllib.request.urlopen(owm_call).read()
            owm_data_str = owm_data.decode('utf8').replace("'", '"')  # for python 3.5 on raspberry !

            json_owm = json.loads(owm_data_str)
            # log_info("\tjson_owm: %s" % str(json_owm))         # test output

            owm_output.append(json_owm['weather'][0]["id"])  # 0
            owm_output.append(json_owm['weather'][0]["description"])  # 1
            owm_output.append(json_owm['weather'][0]["icon"])  # 2; https://openweathermap.org/weather-conditions
            owm_output.append(json_owm['main']['temp'])  # 3
            owm_output.append(json_owm['main']['pressure'])  # 4
            owm_output.append(json_owm['main']['humidity'])  # 5
            owm_output.append(json_owm['main']['temp_min'])  # 6
            owm_output.append(json_owm['main']['temp_max'])  # 7
            owm_output.append(json_owm['wind']['speed'])  # 8

            if 'deg' in json_owm['wind']:
                owm_output.append(json_owm['wind']['deg'])  # 9
            else:
                owm_output.append("0")  # 9

            if 'gust' in json_owm['wind']:
                owm_output.append(json_owm['wind']['gust'])  # 10
            else:
                owm_output.append(0)  # 10

            owm_output.append(json_owm['dt'])  # 11

            log_info("\tLoad OWM - OK")

            yield owm_output
            sleep(delta_time)

    except Exception as ex:
        log_error("\tEx. in - owm(): \n%s" % ex)


if __name__ == '__main__':
    # open_city_json("Minsk", "BY")

    log_info(owm())
