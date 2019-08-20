import json
import sqlite3
import time

from color_log.log_color import (log_verbose, log_warning, log_info, log_error)


def open_json():
    log_verbose("open_json()")
    time_1 = time.perf_counter()

    with open('city.list.json', encoding="utf8") as f:
        data = json.load(f)

    log_warning("\ttime open_json: %s" % (time.perf_counter() - time_1))

    return data


def convert_json_to_db(_data):
    log_verbose("convert_json_to_db()")
    time_2 = time.perf_counter()

    items = 0
    items_zero = 0
    active = False
    purchases = []

    for i in _data:
        if len(i) > 1:
            items += 1

            _id = i['id']
            name = i['name']
            country = i['country']
            coord_lat = i['coord']['lat']
            coord_lon = i['coord']['lon']

            # log_info("%s, %s, %s, %s, %s" % (id, name, country, coord_lat, coord_lon))

            purchase = (_id, name, country, coord_lat, coord_lon, active)
            purchases.append(purchase)
        else:
            items_zero += 1

    log_info("\titems: %s, items_zero: %s" % (items, items_zero))
    log_warning("\ttime_2: " + str(time.perf_counter() - time_2))

    return purchases


def insert_into_db(_data):
    log_verbose("insert_into_db()")
    time_3 = time.perf_counter()

    _db = sqlite3.connect('flask_test.sqlite')
    _cursor = _db.cursor()

    try:
        _cursor.executemany("INSERT INTO owm_city_list "
                            "(id, name, country, coord_lat, coord_lon, active) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            _data)
        _db.commit()
        _db.close()

        log_info("\tinsert_into_db() - OK")

    except sqlite3.DatabaseError as err:
        log_error("\tError: \n%s" % err)
        _db.commit()
        _db.close()

    log_warning("\ttime_3: " + str(time.perf_counter() - time_3))


def set_active_city(_city, _country):
    log_verbose("set_active_city(%s, %s)" % (_city, _country))

    _db = sqlite3.connect('flask_test.sqlite')
    _cursor = _db.cursor()

    try:
        _city_id = _cursor.execute("SELECT id FROM owm_city_list "
                                   "WHERE name = ? AND country = ?",
                                   (_city.title(), _country.upper(),)).fetchone()

        log_info("\tId: %s" % _city_id)
        if _city_id:
            _cursor.execute(
                "UPDATE owm_city_list "
                "SET active = ? "  # set ONE to True
                "WHERE id = ?",
                (True, _city_id[0],)
            )
            _db.commit()

            log_info("\tset_active_city() - OK")
        else:
            log_error("\tset_active_city() - city_id NOT FOUND'")

        _db.close()

    except sqlite3.DatabaseError as err:
        log_error("\tError: \n%s" % err)
        _db.commit()
        _db.close()


if __name__ == '__main__':
    json_data = open_json()
    p = convert_json_to_db(json_data)
    insert_into_db(p)
    set_active_city("Minsk", "BY")
