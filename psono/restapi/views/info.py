from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.conf import settings

# import the logging
from ..utils import log_info
import logging
logger = logging.getLogger(__name__)

class InfoView(GenericAPIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET', 'OPTIONS', 'HEAD')
    throttle_scope = 'health_check'

    def get(self, request, *args, **kwargs):
        """
        Returns the Server's signed information

        :param request:
        :type request:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """

        log_info(logger=logger, request=request, status='HTTP_200_OK', event='READ_INFO_SUCCESS')

        return Response(settings.SIGNATURE, status=status.HTTP_200_OK)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)