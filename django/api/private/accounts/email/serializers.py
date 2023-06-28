from rest_framework import serializers
import os

# Models
from domain.taigas.models.Account import Account

import logging
logger = logging.getLogger(__name__)


class AccountSerializer(serializers.ModelSerializer):
    redirect_url = serializers.SerializerMethodField()

    class Meta:
        ref_name = "private.accounts.email.AccountSerializer"
        model = Account
        fields = [
            'id',
            'username',
            'email',
            'password',
            'project_id',
            'project_name',
            'project_slug',
            'project_description',
            'created_at',
            'updated_at',
            'redirect_url'
        ]

    @staticmethod
    def get_redirect_url(obj):
        redirect_url = os.getenv("TAIGA_REDIRECT_URL")
        return f"{redirect_url}/?email={obj.email}&password={obj.password}"


class ReadAccountSerializer(serializers.Serializer): # noqa

    success = serializers.BooleanField(default=True)
    data = AccountSerializer(source='*')

