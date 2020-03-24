import json
import sqlite3


def parse_city():
    with open('city.list.json', encoding='utf-8') as file:
        cities = json.load(file)

    purchases = []
    active = False

    for city in cities:
        """ {'id': 2750888, 'name': 'Middeldijk', 'country': 'NL', 'coord': {'lon': 4.51667, 'lat': 51.849998} """
        city_id = city['id']
        city_name = city['name']
        country = city['country']
        coord_lng = city['coord']['lon']
        coord_lat = city['coord']['lat']

        purchase = (city_id, city_name, country, coord_lat, coord_lng, active)
        purchases.append(purchase)

    db = sqlite3.connect('../db.sqlite3')
    cursor = db.cursor()

    try:
        cursor.executemany("INSERT INTO forecast_city "
                           "(city_id, name, country, lng, lat, active) "
                           "VALUES (?, ?, ?, ?, ?, ?)",
                           purchases)
        db.commit()
        db.close()

    except sqlite3.DatabaseError as err:
        print("DatabaseError:", err)
        db.commit()
        db.close()

    print('Done')


if __name__ == "__main__":
    parse_city()
