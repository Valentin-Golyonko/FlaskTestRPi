from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('some_view_set', SomeViewSet, basename='some_view_set')

urlpatterns = router.urls

urlpatterns += [
    # path('', SomeView, name=''),
]
