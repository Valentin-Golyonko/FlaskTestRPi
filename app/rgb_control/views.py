from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.rgb_control.rgb_control_scripts.get_rgb_divice import GetRGBDevice
from config.settings import LOGOUT_REDIRECT_URL


class RGBControlView(LoginRequiredMixin, GenericAPIView):
    login_url = LOGOUT_REDIRECT_URL
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'rgb_control/rgb_control_main.html'
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(
            data={
                'some_data': 'some_data',
                "rgb_device": GetRGBDevice.device_serialized_data(),
            },
            status=status.HTTP_200_OK
        )
