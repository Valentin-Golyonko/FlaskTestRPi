from django.urls import path

from sensors.views import SensorsView

urlpatterns = [
    path('', SensorsView.as_view(), name='sensors'),
]
