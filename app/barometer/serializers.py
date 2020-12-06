from rest_framework import serializers

from app.barometer.models import Barometer
from app.core.serializers import DeviceSerializer


class BarometerSerializer(serializers.ModelSerializer):
    device = DeviceSerializer()

    class Meta:
        model = Barometer
        fields = (
            'temperature_c',
            'humidity',
            'pressure_hpa',
            'device',
            'time_created',
        )
