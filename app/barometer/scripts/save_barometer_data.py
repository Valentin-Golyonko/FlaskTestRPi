import logging

from app.barometer.models import Barometer
from app.core.models import Device

logger = logging.getLogger(__name__)


class SaveBarometerData:

    @classmethod
    def save_barometer_data(cls, **kwargs) -> None:
        try:
            device_obj = kwargs.get('device_obj')

            Barometer.objects.create(
                temperature_c=kwargs.get('temperature_c'),
                humidity=kwargs.get('humidity'),
                pressure_hpa=kwargs.get('pressure_hpa'),
                device=device_obj,
            )
        except Exception as ex:
            logger.exception(f"save_barometer_data(): {ex}")
        else:
            cls.limit_saved_data(device_obj)

    @staticmethod
    def limit_saved_data(device_obj: Device) -> None:
        """ limit data to 1008 = 6 saves per hour (1 in 10 min) * 24 hours * 7 days """
        all_data_ids = [i.id for i in Barometer.objects.filter(device=device_obj) if i]
        if len(all_data_ids) > 1008:
            Barometer.objects.filter(id__in=all_data_ids[1007::-1], device=device_obj).delete()
