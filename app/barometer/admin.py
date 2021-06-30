from django.contrib import admin

from app.barometer.models import Barometer
from config.settings import DEBUG

if DEBUG:
    @admin.register(Barometer)
    class BarometerAdmin(admin.ModelAdmin):
        list_display = (
            'device',
            'temperature_c',
            'humidity',
            'pressure_hpa',
            'time_created',
        )
        readonly_fields = (
            'temperature_c',
            'humidity',
            'pressure_hpa',
            'device',
            'time_created',
        )
