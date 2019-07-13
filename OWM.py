"""
Weather API:
    https://openweathermap.org/api
"""
import json
import urllib.request

import api_keys.keys as key
from color_log.log_color import log_info, log_verbose, log_error


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


def owm():
    log_verbose("owm()")

    id_city = open_city_json("Minsk", "BY")

    owm_output = []
    try:
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

        log_info("\tLoad OWM OK")

    except Exception as ex:
        log_error("\towm(): \n%s" % ex)

    return owm_output


if __name__ == '__main__':
    # open_city_json("Minsk", "BY")

    log_info(owm())
