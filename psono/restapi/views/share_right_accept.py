from .share_tree import create_share_link
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from ..utils import readbuffer
from ..authentication import TokenAuthentication

from ..app_settings import (
    ShareRightAcceptSerializer,
)

# import the logging
from ..utils import log_info
import logging
logger = logging.getLogger(__name__)

class ShareRightAcceptView(GenericAPIView):
    """
    Check the REST Token and the object permissions and updates the share right as accepted with new symmetric
    encryption key and nonce
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, *args, **kwargs):
        """
        Mark a Share_right as accepted. In addition update the share right with the new encryption key and deletes now
        unnecessary information like title.

        :param request:
        :param args:
        :param kwargs:
        :return: 200 / 400
        """

        serializer = ShareRightAcceptSerializer(data=request.data, context=self.get_serializer_context())

        if not serializer.is_valid():

            log_info(logger=logger, request=request, status='HTTP_400_BAD_REQUEST', event='ACCEPT_SHARE_RIGHT_ERROR', errors=serializer.errors)

            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        user_share_right_obj = serializer.validated_data.get('user_share_right_obj')

        # Deprecated
        if request.data.get('link_id', False) and not create_share_link(request.data['link_id'], user_share_right_obj.share_id,
                                                                        serializer.validated_data.get('parent_share_id'),
                                                                        serializer.validated_data.get('parent_datastore_id')):

            log_info(logger=logger, request=request, status='HTTP_400_BAD_REQUEST', event='ACCEPT_SHARE_RIGHT_LIK_ID_DUPLICATE_ERROR')

            return Response({"message": "Link id already exists.",
                             "resource_id": request.data['share_right_id']}, status=status.HTTP_400_BAD_REQUEST)

        type = user_share_right_obj.type
        type_nonce = user_share_right_obj.type_nonce

        user_share_right_obj.accepted = True
        user_share_right_obj.type = ''
        user_share_right_obj.type_nonce = ''
        user_share_right_obj.key_type = serializer.validated_data.get('key_type', False)

        if serializer.validated_data.get('key', False):
            user_share_right_obj.key = serializer.validated_data.get('key')
        if serializer.validated_data.get('key_nonce', False):
            user_share_right_obj.key_nonce = serializer.validated_data.get('key_nonce')

        user_share_right_obj.save()

        log_info(logger=logger, request=request, status='HTTP_200_OK', event='ACCEPT_SHARE_RIGHT_SUCCESS', request_resource=request.data['share_right_id'])

        if user_share_right_obj.read:

            return Response({
                "share_id": user_share_right_obj.share.id,
                "share_data": readbuffer(user_share_right_obj.share.data),
                "share_data_nonce": user_share_right_obj.share.data_nonce,
                "share_type": type,
                "share_type_nonce": type_nonce
            }, status=status.HTTP_200_OK)

        return Response({
            "share_id": user_share_right_obj.share.id,
            "share_type": type,
            "share_type_nonce": type_nonce
        }, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


