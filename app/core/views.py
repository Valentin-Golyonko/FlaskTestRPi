from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.tasks import task_celery_test_run


class CeleryTestRunAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def get(cls, request, *args, **kwargs):
        result = task_celery_test_run.delay()
        out_data = {'result': result.get()}
        return Response(data=out_data, status=status.HTTP_200_OK)
