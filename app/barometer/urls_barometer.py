from django.urls import path
from rest_framework import routers

from app.barometer.views import BarometerViewSet

router = routers.DefaultRouter()
router.register('barometers', BarometerViewSet, basename='barometers')

urlpatterns = router.urls

urlpatterns += [
    # path('', SomeView, name=''),
]
