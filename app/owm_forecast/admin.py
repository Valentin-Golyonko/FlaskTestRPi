from django.contrib import admin

from app.owm_forecast.models import Forecast


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'city',
        'units',
        'is_main_source',
    ]

    def is_main_source(self, obj: Forecast) -> bool:
        return bool(obj.main_source)

    is_main_source.boolean = True
