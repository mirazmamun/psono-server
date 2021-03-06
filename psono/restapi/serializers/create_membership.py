from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions
from ..fields import UUIDField, BooleanField
from ..models import User, User_Group_Membership

import re

class CreateMembershipSerializer(serializers.Serializer):

    user_id = UUIDField(required=True)
    group_id = UUIDField(required=True)
    secret_key = serializers.CharField(required=True)
    secret_key_nonce = serializers.CharField(max_length=64, required=True)
    secret_key_type = serializers.CharField(default='asymmetric')
    private_key = serializers.CharField(required=True)
    private_key_nonce = serializers.CharField(max_length=64, required=True)
    private_key_type = serializers.CharField(default='asymmetric')
    group_admin = BooleanField(default=False)
    share_admin = BooleanField(default=True)

    def validate_secret_key(self, value):
        value = value.strip()

        if not re.match('^[0-9a-f]*$', value, re.IGNORECASE):
            msg = _('secret_key must be in hex representation')
            raise exceptions.ValidationError(msg)

        return value

    def validate_secret_key_nonce(self, value):
        value = value.strip()

        if not re.match('^[0-9a-f]*$', value, re.IGNORECASE):
            msg = _('secret_key_nonce must be in hex representation')
            raise exceptions.ValidationError(msg)

        return value

    def validate_secret_key_type(self, value):
        value = value.strip()

        if value not in ('symmetric', 'asymmetric'):
            msg = _('Unknown secret key type')
            raise exceptions.ValidationError(msg)

        return value

    def validate_private_key(self, value):
        value = value.strip()

        if not re.match('^[0-9a-f]*$', value, re.IGNORECASE):
            msg = _('private_key must be in hex representation')
            raise exceptions.ValidationError(msg)

        return value

    def validate_private_key_nonce(self, value):
        value = value.strip()

        if not re.match('^[0-9a-f]*$', value, re.IGNORECASE):
            msg = _('private_key_nonce must be in hex representation')
            raise exceptions.ValidationError(msg)

        return value

    def validate_private_key_type(self, value):
        value = value.strip()

        if value not in ('symmetric', 'asymmetric'):
            msg = _('Unknown private key type')
            raise exceptions.ValidationError(msg)

        return value

    def validate_user_id(self, value):

        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            msg = _('Target user does not exist.')
            raise exceptions.ValidationError(msg)

        return value

    def validate_group_id(self, value):

        try:
            # This line also ensures that the desired group exists and that the user firing the request has admin rights
            User_Group_Membership.objects.get(group_id=value, user=self.context['request'].user, group_admin=True, accepted=True)
        except User_Group_Membership.DoesNotExist:
            msg = _("You don't have permission to access or it does not exist.")
            raise exceptions.ValidationError(msg)

        return value
