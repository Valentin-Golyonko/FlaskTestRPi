from rest_framework import routers

from app.barometer.views import BarometerViewSet

router = routers.DefaultRouter()
router.register('barometers', BarometerViewSet, basename='barometers')

urlpatterns = router.urls

urlpatterns += [
    # path('SomeView/', SomeView, name='SomeView'),
]
