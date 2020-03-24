import os

import requests
from django.shortcuts import render
from django.views.generic import TemplateView

from forecast.models import City


class Forecast(TemplateView):
    template_name = 'forecast/forecast.html'

    def get(self, request, *args, **kwargs):
        city_id = City.objects.get(name='Minsk', country='BY').city_id
        forecast_url = "http://api.openweathermap.org/data/2.5/weather?" \
                       "id=%s&units=metric&appid=%s" % (city_id, os.environ.get('OWM_API_KEY'))
        forecast_response = requests.get(forecast_url)
        if forecast_response.ok:
            forecast_json = forecast_response.json()
        else:
            forecast_json = None

        response = {'forecast': forecast_json, }
        return render(request=request, template_name=self.template_name, context=response)
