from django.urls import path
from rest_framework import routers

from app.rgb_control.views import (
    RGBControlAPIView, SendColorAPIView
)

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('rgb_controls/', RGBControlAPIView.as_view(), name='rgb_controls'),
    path('send_color/', SendColorAPIView.as_view(), name='send_color'),
]
