from django.urls import path
from rest_framework import routers

from app.core.views import CeleryTestRunAPIView

router = routers.DefaultRouter()
# router.register('some_view_set', SomeViewSet, basename='some_view_set')

urlpatterns = router.urls

urlpatterns += [
    path('celery_test_run/', CeleryTestRunAPIView.as_view(), name='celery_test_run'),
]
