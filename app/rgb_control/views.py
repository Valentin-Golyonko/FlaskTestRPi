from asgiref.sync import async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from app.rgb_control.rgb_control_scripts.get_rgb_divice import GetRGBDevice
from app.rgb_control.rgb_control_scripts.set_led_strip_color import SetLEDStripColor
from app.rgb_control.serializers import SendColorSerializer
from config.settings import LOGOUT_REDIRECT_URL


class RGBControlAPIView(LoginRequiredMixin, GenericAPIView):
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


class SendColorAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    serializer_class = SendColorSerializer

    @async_to_sync
    async def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_ok, error_msg = await SetLEDStripColor.set_rgb_strip_color(serializer.validated_data)

        if is_ok:
            return Response(data='hello world', status=status.HTTP_200_OK)
        return Response(data=error_msg, status=status.HTTP_400_BAD_REQUEST)
