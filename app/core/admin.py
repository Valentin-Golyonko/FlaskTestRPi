from django.contrib import admin

from app.core.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
        'i2c_address',
        'ip_address',
        'mac_address',
    )
    list_display = (
        'title',
        'device_type',
        'sub_type',
        'address_type',
        'i2c_address_',
        'ip_address_',
        'mac_address_',
        'is_alive',
        'last_update',
    )

    def i2c_address_(self, obj) -> bool:
        return bool(obj.i2c_address)

    i2c_address_.boolean = True

    def ip_address_(self, obj) -> bool:
        return bool(obj.ip_address)

    ip_address_.boolean = True

    def mac_address_(self, obj) -> bool:
        return bool(obj.mac_address)

    mac_address_.boolean = True
