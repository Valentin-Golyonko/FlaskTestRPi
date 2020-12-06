from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app.core.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('api/core/', include('app.core.urls_core')),
    path('api/barometer/', include('app.barometer.urls_barometer')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
