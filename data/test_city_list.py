import json
import sqlite3


def open_json():
    with open('city.list.json', encoding="utf8") as f:
        data = json.load(f)
    return data


def json_open_test(_data):
    """ EX: 596826, Murava, LT, 54.916672, 23.966669
    items: 209579, items_zero: 0

    :param _data:
    :return:
    """
    items = 0
    items_zero = 0

    for i in _data:
        if len(i) > 1:
            items += 1

            _id = i['id']
            name = i['name']
            country = i['country']
            coord_lat = i['coord']['lat']
            coord_lon = i['coord']['lon']

            # log_info("%s, %s, %s, %s, %s" % (_id, name, country, coord_lat, coord_lon))
        else:
            items_zero += 1

    print(items, items_zero)


def db_test(city, country):
    i_db = sqlite3.connect('flask_test.sqlite')
    i_cursor = i_db.cursor()

    try:
        _id = i_cursor.execute("SELECT id FROM owm_city_list "
                               "WHERE name = ? AND country = ?",
                               (city.title(), country.upper(),)).fetchone()
        print(_id)
        i_db.close()

    except sqlite3.DatabaseError as err:
        print("\tError: \n%s" % err)
        i_db.commit()
        i_db.close()


def test():
    """
    >>> json_open_test(open_json())
    209579 0
    >>> db_test("Minsk", "BY")
    (625144,)
    """
