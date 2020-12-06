from rest_framework import serializers

from app.core.models import Device


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = (
            'title',
            'device_type',
            'sub_type',
            'address_type',
            'i2c_address',
            'ip_address',
        )
