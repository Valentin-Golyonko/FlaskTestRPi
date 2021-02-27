import logging
from typing import Optional

import requests

from app.owm_forecast.models import Forecast

logger = logging.getLogger(__name__)


class ForecastData:

    @classmethod
    def do_owm_request(cls, weather: bool, air_pollution: bool) -> None:
        forecast_obj = Forecast.objects.filter(main_source=True).first()
        if forecast_obj:
            response_weather = None
            response_air_pollution = None
            if weather:
                try:
                    response_weather = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather"
                        f"?q={forecast_obj.city}"
                        f"&appid={forecast_obj.api_key}"
                        f"&units={forecast_obj.get_units_display()}"
                    ).json()
                except Exception as ex:
                    logger.error(f"do_owm_request(): {ex}")

            if air_pollution:
                try:
                    response_air_pollution = requests.get(
                        f"http://api.openweathermap.org/data/2.5/air_pollution"
                        f"?lat={forecast_obj.geo_coord.get('lat')}"
                        f"&lon={forecast_obj.geo_coord.get('lon')}"
                        f"&appid={forecast_obj.api_key}"
                    ).json()
                except Exception as ex:
                    logger.error(f"do_owm_request(): {ex}")

            if response_weather or response_air_pollution:
                cls.save_owm_data(
                    forecast_obj=forecast_obj,
                    weather_data=response_weather,
                    air_pollution_data=response_air_pollution,
                )
        else:
            logger.error(f"do_owm_request(): forecast_obj is None.")

    @staticmethod
    def save_owm_data(forecast_obj: Forecast,
                      weather_data: Optional[dict],
                      air_pollution_data: Optional[dict]) -> None:
        new_data = False
        try:
            if weather_data:
                forecast_obj.current_weather_data = weather_data
                forecast_obj.geo_coord = weather_data.get('coord')
                new_data = True

            if air_pollution_data:
                forecast_obj.current_air_pollution_data = air_pollution_data
                new_data = True

            if new_data:
                forecast_obj.save()
        except Exception as ex:
            logger.exception(f"save_owm_data(): {ex}")
