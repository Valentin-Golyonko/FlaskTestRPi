from rest_framework import mixins
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)
