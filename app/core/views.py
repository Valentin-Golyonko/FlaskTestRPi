from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.core.tasks import task_celery_test_run
from config.settings import LOGOUT_REDIRECT_URL


class CeleryTestRunAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, *args, **kwargs):
        result = task_celery_test_run.delay()
        out_data = {'result': result.get()}
        return Response(data=out_data, status=status.HTTP_200_OK)


class MainPageView(LoginRequiredMixin, GenericAPIView):
    login_url = LOGOUT_REDIRECT_URL
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/main_page.html'
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return Response({'main_page_data': 'Hello world'})


class LogInView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/login_view.html'
    permission_classes = (AllowAny,)
    pagination_class = None

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
