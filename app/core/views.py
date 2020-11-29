from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class SimpleAPIView(APIView):
    authentication_classes = None
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_page.html'

    @classmethod
    def get(cls, request, *args, **kwargs):
        return Response(data={'serializer': ''}, status=status.HTTP_200_OK)
