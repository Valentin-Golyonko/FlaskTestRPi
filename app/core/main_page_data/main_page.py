from django.utils.timezone import localtime

from app.barometer.models import Barometer
from app.barometer.serializers import BarometerSerializer


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
        return {'forecast': None}
