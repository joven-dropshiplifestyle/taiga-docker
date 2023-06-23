from rest_framework import serializers

# Models
from domain.taigas.models import Account

import logging
logger = logging.getLogger(__name__)


class ReadAccountSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "private.registration.ReadAccountSerializer"
        model = Account
        fields = [
            'id',
            'email',
            'project_id',
            'project_name',
            'project_slug',
            'project_description',
            'created_at',
            'updated_at'
        ]


class AccountAlreadyExistSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.registration.AccountAlreadyExistSerializer"

    message = serializers.CharField()


class CreateAccountSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.registration.CreateAccountSerializer"

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    project_name = serializers.CharField()
    project_description = serializers.CharField()
