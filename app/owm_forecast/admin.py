from django.contrib import admin

from app.owm_forecast.models import Forecast


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    pass
