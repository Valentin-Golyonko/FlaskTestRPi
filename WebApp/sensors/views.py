from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from sensors.forms import NewSensor
from sensors.models import Sensors


class SensorsView(TemplateView):
    template_name = 'sensors/sensors.html'

    def get(self, request, *args, **kwargs):
        response = {
            "new_sensor_form": NewSensor(),
            "all_sensors": Sensors.objects.all(),
        }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request, *args, **kwargs):
        new_sensor_form = NewSensor(request.POST)
        if new_sensor_form.is_valid():
            new_sensor_form.save()
        else:
            print('NewSensor Form invalid!')

        return reverse_lazy('sensors')
