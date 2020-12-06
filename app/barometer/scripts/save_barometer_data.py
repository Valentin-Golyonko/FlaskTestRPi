import logging

from app.barometer.models import Barometer

logger = logging.getLogger(__name__)


class SaveBarometerData:

    @staticmethod
    def save_barometer_data(**kwargs) -> None:
        try:
            barometer = Barometer(
                temperature_c=kwargs.get('temperature_c'),
                humidity=kwargs.get('humidity'),
                pressure_hpa=kwargs.get('pressure_hpa'),
            )
            barometer.save()
        except Exception as ex:
            logger.exception(f"save_barometer_data(): {ex}.")
