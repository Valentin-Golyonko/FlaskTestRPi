from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.owm_forecast.models import Forecast
from config.settings import LOGOUT_REDIRECT_URL


class ForecastView(LoginRequiredMixin, GenericAPIView):
    login_url = LOGOUT_REDIRECT_URL
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'forecast/forecast.html'
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @staticmethod
    def get(request, *args, **kwargs):
        forecast_obj = Forecast.objects.filter(main_source=True).first()
        if forecast_obj:
            weather_data = forecast_obj.current_weather_data if forecast_obj.current_weather_data else {}
            air_pollution_data = forecast_obj.current_air_pollution_data if forecast_obj.current_air_pollution_data else {}
            return Response(
                data={**weather_data,
                      **air_pollution_data,
                      },
                status=status.HTTP_200_OK
            )
        else:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
