from django.urls import path
from rest_framework import routers

from app.core.views import SimpleAPIView

router = routers.DefaultRouter()
# router.register('some_view_set', SomeViewSet, basename='some_view_set')

urlpatterns = router.urls

urlpatterns += [
    path('', SimpleAPIView.as_view(), name='simple_view'),
]
