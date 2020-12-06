from django.contrib import admin

from app.core.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
        'i2c_address',
        'ip_address',
    )
    list_display = (
        'title',
        'device_type',
        'sub_type',
        'address_type',
        'i2c_address',
        'ip_address',
    )
