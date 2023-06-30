from rest_framework import serializers

import logging
logger = logging.getLogger(__name__)


class ProjectSerializer(serializers.Serializer): # noqa
    class Meta:
        ref_name = "management.epics.id.duplicate.ProjectSerializer"

    project_slug = serializers.SlugField()



class ResponseSerializer(serializers.Serializer): # noqa
    class Meta:
        ref_name = "management.epics.id.duplicate.ResponseSerializer"

    message = serializers.CharField()
