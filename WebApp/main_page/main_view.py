from django.shortcuts import render
from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'main_page/main_page.html'

    def get(self, request, *args, **kwargs):
        response = {}
        return render(request=request, template_name=self.template_name, context=response)
