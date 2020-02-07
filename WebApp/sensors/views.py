from django.shortcuts import render
from django.views.generic import TemplateView


class Sensors(TemplateView):
    template_name = 'sensors/sensors.html'

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.template_name, context={})
