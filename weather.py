"""
Weather API:
    https://openweathermap.org/api
"""
from datetime import datetime
from json import loads
from sqlite3 import connect
from time import sleep
from urllib.request import urlopen

from flask import (
    Blueprint, render_template, request, redirect, url_for)

from .api_keys.keys import owm_api_key
from .color_log.log_color import log_verbose, log_error, log_info, log_warning
from .db import get_db, close_db

bp = Blueprint('weather', __name__)


@bp.route('/weather', methods=('GET', 'POST', 'PUT'))
def index():
    log_verbose("weather: index()")

    if request.method == 'POST':
        city = request.form['city']

        if city:
            city = str(city).split()
            set_city(city)
            upd_db_new_city()

    forecast = owm_forecast()

    db_row_data = get_owm_data()[0]

    if db_row_data:
        data = [i for i in db_row_data]

        data[12] = datetime.fromtimestamp(data[12])  # convert from unix time to local time
        # log_info("\tlast owm time: %s (%s)" % (data[12], type(data[12])))  # test print

        return render_template('weather/weather.html', owm_db_data=[data, forecast])
    else:
        log_warning("redirect to 'smart_home.index'")
        return redirect(url_for('smart_home.index'))


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

        if owm_db_data:
            return owm_db_data
        else:
            log_error("\tget_owm_data()\nNO DATA in the 'owm_db_data' table")
    except Exception as ex:
        log_error("\tEx. in - get_owm_data():\n%s" % ex)
        close_db()


def set_city(city):
    log_verbose("set_city()")
    try:
        db = get_db()
        cur = get_db().cursor()
        city_id = cur.execute("SELECT id FROM owm_city_list "
                              "WHERE name = ? AND country = ?",
                              (city[0], city[1],)).fetchone()[0]
        if city_id:
            cur.execute(
                "UPDATE owm_city_list SET active = 0"  # reset all
            )
            db.commit()

            cur.execute(
                "UPDATE owm_city_list SET active = ?"  # set ONE to True
                " WHERE id = ?",
                (True, city_id,)
            )
            db.commit()
            close_db()
            log_info("\tset_city() - OK")
        else:
            log_error("\tset_city() - city_id NOT FOUND\nredirect to 'smart_home.index'")
            redirect(url_for('smart_home.index'))
    except Exception as ex:
        log_error("\tEx. in - set_city():\n%s" % ex)
        close_db()


def update_owm_db_table():
    log_verbose("update_owm_db_table()")
    _owm = owm(600)  # default timer = 10 min
    try:
        while True:
            owm_data = next(_owm)
            if owm_data:
                db = connect("data/flask_test.sqlite")
                # db = get_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO owm (weather_id, description,"
                               " icon, temp, pressure, humidity, temp_min,"
                               " temp_max, wind_speed, wind_deg, wind_gust, time_unix)"
                               " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", owm_data)

                db.commit()
                db.close()
                log_info("\tupdate_owm_db_table() - OK")
            else:
                log_error("\tupdate_owm_db_table()\nNo data from owm()")
    except Exception as ex:
        log_error("\tEx. in - update_owm_db_table():\n%s" % ex)


def owm(delta_time=600):
    log_verbose("owm()")
    try:
        while True:
            db = connect("data/flask_test.sqlite")
            cur = db.cursor()
            city_id = cur.execute("SELECT id FROM owm_city_list "
                                  "WHERE active = ?",
                                  (True,)).fetchone()[0]
            db.close()
            # log_info("\towm() - city_id: %s" % city_id)

            if city_id:
                owm_output = []
                owm_call = "http://api.openweathermap.org/data/2.5/weather?id=" + \
                           str(city_id) + "&units=metric&APPID=" + str(owm_api_key)

                owm_data = urlopen(owm_call).read()
                owm_data_str = owm_data.decode('utf8').replace("'", '"')  # for python 3.5 on raspberry !

                json_owm = loads(owm_data_str)
                # log_info("\tjson_owm: %s" % json_owm)         # test output

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
                    owm_output.append(0)  # 9

                if 'gust' in json_owm['wind']:
                    owm_output.append(json_owm['wind']['gust'])  # 10
                else:
                    owm_output.append(0)  # 10

                owm_output.append(json_owm['dt'])  # 11

                log_info("\tLoad owm() - OK")

                yield owm_output
                sleep(delta_time)

            else:
                log_error("\towm() - city_id NOT FOUND\nretry in 1 min")
                yield None
                sleep(60)

    except Exception as ex:
        log_error("\tEx. in - owm():\n%s" % ex)


def upd_db_new_city():
    log_verbose("upd_db_new_city()")
    _owm = owm()
    try:
        _data = next(_owm)
        if _data:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO owm (weather_id, description,"
                           " icon, temp, pressure, humidity, temp_min,"
                           " temp_max, wind_speed, wind_deg, wind_gust, time_unix)"
                           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", _data)
            db.commit()
            close_db()
            log_info("\tupd_db_new_city - OK")
        else:
            log_error("\tNo data from owm()")
    except Exception as ex:
        log_error("\tEx. in - upd_db_new_city: \n%s" % ex)
        close_db()


def owm_forecast():
    log_verbose("owm_forecast()")
    try:
        while True:
            db = connect("data/flask_test.sqlite")
            cur = db.cursor()
            city_id = cur.execute("SELECT id FROM owm_city_list "
                                  "WHERE active = ?",
                                  (True,)).fetchone()[0]
            db.close()
            # log_info("\towm() - city_id: %s" % city_id)

            if city_id:
                owm_call = "http://api.openweathermap.org/data/2.5/forecast?id=" + \
                           str(city_id) + "&units=metric&APPID=" + str(owm_api_key)

                owm_data = urlopen(owm_call).read()
                owm_data_str = owm_data.decode('utf8').replace("'", '"')  # for python 3.5 on raspberry !

                json_owm = loads(owm_data_str)
                # log_info("\tjson_owm: %s" % json_owm)         # test output

                # with open('data/f.json') as f:
                #     json_owm = json.loads(f.read())
                #     log_info("\tJSON LOADED\n%s" % json_owm)

                forecast_len = len(json_owm['list'])
                for i in range(forecast_len):
                    # convert from unix time to local time
                    json_owm['list'][i]['dt'] = datetime.fromtimestamp(json_owm['list'][i]['dt']).strftime('%A %b %d')

                log_info("\tLoad owm_forecast() - OK")

                return json_owm
                # sleep(delta_time)

            else:
                log_error("\towm_forecast() - city_id NOT FOUND")
                return None
                # sleep(60)

    except Exception as ex:
        log_error("\tEx. in - owm_forecast():\n%s" % ex)


if __name__ == '__main__':
    # open_city_json("Minsk", "BY")

    log_info(owm())
