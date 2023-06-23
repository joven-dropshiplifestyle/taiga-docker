from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)


class QuerySerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.authenticate.QuerySerializer"

    email = serializers.EmailField()


class ReadUserInfoSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.authenticate.ReadUserInfoSerializer"

    id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    full_name_display = serializers.CharField()
    color = serializers.CharField()
    bio = serializers.CharField()
    lang = serializers.CharField()
    theme = serializers.CharField()
    timezone = serializers.CharField()
    is_active = serializers.BooleanField()
    photo = serializers.CharField(allow_null=True)
    big_photo = serializers.CharField(allow_null=True)
    gravatar_id = serializers.CharField()
    roles = serializers.ListField(child=serializers.CharField())
    total_private_projects = serializers.IntegerField()
    total_public_projects = serializers.IntegerField()
    email = serializers.EmailField()
    uuid = serializers.CharField()
    date_joined = serializers.DateTimeField()
    read_new_terms = serializers.BooleanField()
    accepted_terms = serializers.BooleanField()
    max_private_projects = serializers.CharField(allow_null=True)
    max_public_projects = serializers.CharField(allow_null=True)
    max_memberships_private_projects = serializers.CharField(allow_null=True)
    max_memberships_public_projects = serializers.CharField(allow_null=True)
    verified_email = serializers.BooleanField()
    refresh = serializers.CharField()
    auth_token = serializers.CharField()


class ReadAuthCredentialSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "private.authenticate.ReadAuthCredentialSerializer"

    user_info = ReadUserInfoSerializer()
    token = serializers.CharField()
    refresh = serializers.CharField()
