from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.barometer.models import Barometer
from app.barometer.serializers import BarometerSerializer


class BarometerViewSet(mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'barometer/barometer.html'
    permission_classes = (IsAuthenticated,)
    queryset = Barometer.objects.all()
    serializer_class = BarometerSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        query_list = list(self.filter_queryset(self.get_queryset()))
        if not query_list:
            return Response(data={}, status=status.HTTP_200_OK)

        x_axis_limit = 10

        last_obj = query_list[-1]
        if len(query_list) >= x_axis_limit:
            last_x_obj = query_list[-x_axis_limit]
        else:
            last_x_obj = query_list[0]

        out_data = {
            'temperature_c': [],
            'humidity': [],
            'pressure_hpa': [],
            'device': [],
            'time_created': [],
            'xaxis_range': [
                last_x_obj.time_created.strftime('%Y-%m-%d %H:%M'),
                last_obj.time_created.strftime('%Y-%m-%d %H:%M')
            ],
        }

        for data_obj in query_list:
            out_data.get('temperature_c').append(float(data_obj.temperature_c))
            out_data.get('humidity').append(float(data_obj.humidity))
            out_data.get('time_created').append(data_obj.time_created.strftime('%Y-%m-%d %H:%M'))

        return Response(data=out_data, status=status.HTTP_200_OK)
