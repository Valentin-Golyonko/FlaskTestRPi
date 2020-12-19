from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.core.serializers import LoginSerializer
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

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class LogInView(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/login_view.html'
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = LoginSerializer

    def get(self, request, *args, **kwargs):
        return Response(data={'serializer': self.get_serializer()}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data.get('username'),
            password=serializer.validated_data.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
