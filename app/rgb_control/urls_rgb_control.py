from django.urls import path
from rest_framework import routers

from app.rgb_control.views import RGBControlView

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path('rgb_controls/', RGBControlView.as_view(), name='rgb_controls'),
]
