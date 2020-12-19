import logging

import requests

from app.owm_forecast.models import Forecast

logger = logging.getLogger(__name__)


class ForecastData:

    @classmethod
    def get_forecast_data(cls) -> dict:
        forecast_obj = Forecast.objects.filter(main_source=True).first()
        if forecast_obj:
            try:
                response = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather"
                    f"?q={forecast_obj.city}"
                    f"&appid={forecast_obj.api_key}"
                    f"&units={forecast_obj.get_units_display()}"
                ).json()
            except Exception as ex:
                logger.exception(f"forecast(): {ex}.")
                return {}
            else:
                return response
        return {}
