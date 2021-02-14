from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.barometer.models import Barometer
from app.barometer.scripts.collect_barometer_data import CollectBarometerData
from app.barometer.serializers import BarometerSerializer
from config.settings import LOGOUT_REDIRECT_URL


class BarometerViewSet(LoginRequiredMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    login_url = LOGOUT_REDIRECT_URL
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'barometer/barometer.html'
    permission_classes = (IsAuthenticated,)
    queryset = Barometer.objects.all()
    serializer_class = BarometerSerializer
    pagination_class = None

    def get_queryset(self):
        # todo: filter per device
        return Barometer.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(
            data=CollectBarometerData.list_data(
                queryset=self.filter_queryset(self.get_queryset()),
            ),
            status=status.HTTP_200_OK
        )
