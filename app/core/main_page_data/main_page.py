import logging

from django.utils.timezone import localtime

from app.barometer.models import Barometer
from app.barometer.serializers import BarometerSerializer
from app.owm_forecast.models import Forecast

logger = logging.getLogger(__name__)


class MainPage:

    @classmethod
    def get_main_page_data(cls) -> dict:
        return {**cls.latest_in_home(),
                **cls.forecast(),
                }

    @staticmethod
    def latest_in_home() -> dict:
        barometer_obj = Barometer.objects.last()
        barometer_data = BarometerSerializer(barometer_obj).data
        barometer_data['time_created'] = localtime(value=barometer_obj.time_created).time()
        return {'barometer_data': barometer_data}

    @staticmethod
    def forecast() -> dict:
        forecast_obj = Forecast.objects.filter(main_source=True).first()
        if forecast_obj:
            try:
                return {'weather_data': forecast_obj.current_weather_data.get('main', None)}
            except AttributeError:
                pass
        return {}
