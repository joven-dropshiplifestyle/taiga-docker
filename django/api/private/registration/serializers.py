from rest_framework import serializers

# Models
from domain.taigas.models import Account

import logging
logger = logging.getLogger(__name__)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "private.registration.AccountSerializer"
        model = Account
        fields = [
            'id',
            'email',
            'full_name',
            'project_id',
            'project_name',
            'project_slug',
            'project_description',
            'created_at',
            'updated_at'
        ]


class ExistingAccountSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.registration.ExistingAccountSerializer"

    message = serializers.CharField()


class NewAccountSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.registration.NewAccountSerializer"

    username = serializers.CharField()
    full_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    project_name = serializers.CharField()
    project_description = serializers.CharField()
