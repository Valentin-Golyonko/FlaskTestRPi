import logging

from app.barometer.models import Barometer
from app.core.choices import Choices
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
        all_data_ids = Barometer.objects.filter(
            device=device_obj
        ).values_list(
            'id', flat=True
        ).order_by(
            '-time_created'
        )

        if len(all_data_ids) > Choices.BAROMETER_DATA_LIMIT:
            Barometer.objects.exclude(
                id__in=all_data_ids[:Choices.BAROMETER_DATA_LIMIT]
            ).delete()
