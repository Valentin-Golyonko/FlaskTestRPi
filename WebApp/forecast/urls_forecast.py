from django.urls import path

from forecast.views import Forecast

urlpatterns = [
    path('', Forecast.as_view(), name='forecast'),
]
