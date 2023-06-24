from rest_framework import serializers
import os

# Models
from domain.taigas.models.Account import Account

import logging
logger = logging.getLogger(__name__)


class ReadAccountSerializer(serializers.ModelSerializer):
    redirect_url = serializers.SerializerMethodField()

    class Meta:
        ref_name = "private.accounts.email.ReadAccountSerializer"
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
        redirect_url = os.getenv("REDIRECT_URL")
        return f"{redirect_url}/?email={obj.email}&password={obj.password}"
