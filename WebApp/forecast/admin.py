from django.contrib import admin

from forecast.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
