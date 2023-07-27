from rest_framework import serializers

# Validators
from django.core.validators import RegexValidator

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
            'first_name',
            'last_name',
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

    username = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[\w.-]{1,255}$',
                message="Required. 255 characters or fewer. Letters, numbers and ./-/_ characters.",
                code='invalid_username'
            ),
        ],
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    password = serializers.CharField()
    project_name = serializers.CharField()
    project_description = serializers.CharField()
    task_title = serializers.CharField(required=False)
    task_content = serializers.CharField(required=False)
    wiki_content = serializers.CharField(required=False)
