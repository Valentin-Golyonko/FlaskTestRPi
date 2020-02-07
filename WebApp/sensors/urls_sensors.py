from django.urls import path

from sensors.views import Sensors

urlpatterns = [
    path('', Sensors.as_view(), name='sensors'),
]
