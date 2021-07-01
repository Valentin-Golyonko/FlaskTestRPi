from django.urls import path
from rest_framework import routers

from app.core.views import (
    CeleryTestRunAPIView, CommonChoicesApiView
)

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('celery_test_run/', CeleryTestRunAPIView.as_view(), name='celery_test_run'),
    path('common_choices/', CommonChoicesApiView.as_view(), name='common_choices'),
]
