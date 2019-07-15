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
    Blueprint, render_template, request, redirect, url_for)

import api_keys.keys as key
from color_log.log_color import *
from db import get_db, close_db

bp = Blueprint('weather', __name__)


@bp.route('/weather', methods=('GET', 'POST'))
def index():
    log_verbose("weather: index()")

    if request.method == 'POST':
        city = request.form['city']
        if city:
            city = str(city).split()

            set_city(city)
            upd_db_new_city()

    db_row_data = get_owm_data()

    if db_row_data:
        data = [i for i in db_row_data[0]]

        dt = datetime.datetime.utcfromtimestamp(data[12])  # convert from unix time
        log_info("\tlast owm time: " + str(dt))  # test print
        data[11] = str(dt)

        return render_template('weather.html', owm_db_data=data)
    else:
        return redirect(url_for('sensors.index'))


def get_owm_data():
    log_verbose("get_owm_data()")
    try:
        cur = get_db().cursor()
        owm_db_data = cur.execute(
            'SELECT *'
            ' FROM owm'
            ' ORDER BY id DESC LIMIT 1'
        ).fetchall()
        close_db()
        if not owm_db_data:
            log_error("\tget_owm_data() - %s" % owm_db_data)

        return owm_db_data

    except sqlite3.DatabaseError as err:
        log_error("\tEx. in - weather: get_owm_data(): \n%s" % err)
        close_db()


def set_city(city):
    log_verbose("set_city()")
    try:
        db = get_db()
        cur = get_db().cursor()
        city_id = cur.execute("SELECT id FROM owm_city_list "
                              "WHERE name = ? AND country = ?",
                              (city[0], city[1],)).fetchone()[0]

        log_warning("\tset_city - city_id: %s" % city_id)

        cur.execute(
            "UPDATE owm_city_list SET active = 0"
        )
        db.commit()

        cur.execute(
            "UPDATE owm_city_list SET active = ?"
            " WHERE id = ?",
            (True, city_id,)
        )
        db.commit()

        close_db()
        log_info("\tset_city() - OK")

    except Exception as ex:
        log_error("\tEx. in - set_city:\n%s" % ex)
        close_db()


def update_owm_db_table():
    log_verbose("update_owm_db_table()")
    _owm = owm(60)  # timer = 10 min
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
        close_db()


def owm(delta_time=600):
    log_verbose("owm()")

    try:
        while True:
            cur = get_db().cursor()
            city_id = cur.execute("SELECT id FROM owm_city_list "
                                  "WHERE active = ?",
                                  (True,)).fetchone()[0]
            cur.close()
            log_info("\towm, city_id: %s" % city_id)

            owm_output = []
            owm_call = "http://api.openweathermap.org/data/2.5/weather?id=" + \
                       str(city_id) + "&units=metric&APPID=" + str(key.owm_api_key)

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


def upd_db_new_city():
    log_verbose("upd_db_new_city()")
    _owm = owm()
    try:
        _data = next(_owm)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO owm (weather_id, description,"
                       " icon, temp, pressure, humidity, temp_min,"
                       " temp_max, wind_speed, wind_deg, wind_gust, time_unix)"
                       " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", _data)

        db.commit()
        close_db()
        log_info("\tupd_db_new_city - OK")

    except Exception as ex:
        log_error("\tEx. in - upd_db_new_city: \n%s" % ex)
        close_db()


if __name__ == '__main__':
    # open_city_json("Minsk", "BY")

    log_info(owm())
