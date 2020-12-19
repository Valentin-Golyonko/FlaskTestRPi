from django.urls import path
from rest_framework import routers

from app.owm_forecast.views import ForecastView

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('forecasts', ForecastView.as_view(), name='forecasts'),
]
