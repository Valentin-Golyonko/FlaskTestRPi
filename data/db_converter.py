import json
import sqlite3
import time

from color_log.log_color import *


def open_json():
    log_verbose("opening .json")
    time_10 = time.perf_counter()
    with open('city.list.json', encoding="utf8") as f:
        data = json.load(f)

    log_warning("\ttime open_json: %s" % (time.perf_counter() - time_10))

    return data


def test_json_open(_data):
    """ EX: 596826, Murava, LT, 54.916672, 23.966669
    items: 209579, items_zero: 0

    :param _data:
    :return:
    """
    log_verbose("test_json()")
    time_20 = time.perf_counter()

    items = 0
    items_zero = 0

    for i in _data:
        if len(i) > 1:
            items += 1

            id = i['id']
            name = i['name']
            country = i['country']
            coord_lat = i['coord']['lat']
            coord_lon = i['coord']['lon']

            # log_info("%s, %s, %s, %s, %s" % (id, name, country, coord_lat, coord_lon))
        else:
            items_zero += 1

    log_info("\titems: %s, items_zero: %s" % (items, items_zero))
    log_warning("\ttime json_open_test: %s" % (time.perf_counter() - time_20))


def convert_json_to_db(_data):
    log_verbose("convert_json_to_db()")
    time_30 = time.perf_counter()
    items = 0
    items_zero = 0
    active = False
    purchases = []

    i_db = sqlite3.connect('flask_test.sqlite')
    i_cursor = i_db.cursor()

    for i in _data:
        if len(i) > 1:
            items += 1

            id = i['id']
            name = i['name']
            country = i['country']
            coord_lat = i['coord']['lat']
            coord_lon = i['coord']['lon']

            # log_info("%s, %s, %s, %s, %s" % (id, name, country, coord_lat, coord_lon))

            purchase = (id, name, country, coord_lat, coord_lon, active)
            purchases.append(purchase)
        else:
            items_zero += 1

    log_info("\titems: %s, items_zero: %s" % (items, items_zero))
    log_warning("\ttime_3.1: " + str(time.perf_counter() - time_30))

    time_32 = time.perf_counter()
    try:
        i_cursor.executemany("INSERT INTO owm_city_list "
                             "(id, name, country, coord_lat, coord_lon, active) "
                             "VALUES (?, ?, ?, ?, ?, ?)",
                             purchases)
        i_db.commit()
        i_db.close()

    except sqlite3.DatabaseError as err:
        log_error("\tError: \n%s" % err)
        i_db.commit()
        i_db.close()

    log_warning("\ttime_3.2: " + str(time.perf_counter() - time_32))
    log_warning("\ttime_3.0: " + str(time.perf_counter() - time_30))


def test_db(_str):
    log_verbose("open_db()")
    time_40 = time.perf_counter()

    i_db = sqlite3.connect('flask_test.sqlite')
    i_cursor = i_db.cursor()

    try:
        _id, city = i_cursor.execute("SELECT id, name FROM owm_city_list WHERE name = ?", (_str,)).fetchone()
        log_info("\t%s - %s" % (_id, city))
        i_db.close()

    except sqlite3.DatabaseError as err:
        log_error("\tError: \n%s" % err)
        i_db.commit()
        i_db.close()

    log_warning("\ttime_6.1: " + str(time.perf_counter() - time_40))


if __name__ == '__main__':
    """
    >>> test_json_open(open_json())
    items: 209579, items_zero: 0
    >>> test_db("Minsk")
    625144 - Minsk
    """

    db_data = open_json()

    test_json_open(db_data)

    convert_json_to_db(db_data)

    test_db("Minsk")
