from typing import Any, Tuple, Dict

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Serializers
from .serializers import ProjectSerializer, ResponseSerializer

# Taiga Integration
from domain.taigas.integrations.integration_projects import get_project_id_by_slug
from domain.taigas.integrations.integration_userstories import get_user_stories_by_epic_from_template_project, \
    create_user_stories, link_user_stories_to_epic
from domain.taigas.integrations.integration_epics import create_epic, get_epic_id_from_project_template_by_ref_id

# Permission
from domain.users.permissions.permission_header import HeaderKeyPermission

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json
import logging

logger = logging.getLogger(__name__)


class EpicsRefRefIdDuplicateAPIView(APIView):
    permission_classes = (HeaderKeyPermission,)

    @staticmethod
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'X-SPECIAL-KEY',
                openapi.IN_HEADER,
                description="special key to access this API",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=ProjectSerializer,
        operation_id="epics_duplicate",
        tags=["management.epics"],
        responses={
            200: ResponseSerializer(),
        }
    )
    def post(request: Request, ref_id=None) -> Response:
        logger.info(f"Authenticated user: {request.user}")

        # Validate Request Data
        logger.info(request.data)
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)

        project_slug = project_serializer.validated_data['project_slug']

        # Get Project ID
        project_id = get_project_id_by_slug(slug=project_slug)
        if not project_slug:
            return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get Epic ID
        epic_id = get_epic_id_from_project_template_by_ref_id(ref_id=ref_id)
        if not epic_id:
            return Response({"detail": "Ref not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get Epic User Stories
        user_stories = get_user_stories_by_epic_from_template_project(epic_id=epic_id)
        if not user_stories:
            return Response({"detail": "Epic not found."}, status=status.HTTP_404_NOT_FOUND)

        # Create Epic to Project
        logger.info(user_stories[0])
        created_epic_id = create_epic(user_stories[0], project_id=project_id)
        logger.info(f"epic: {created_epic_id}")
        if not user_stories:
            return Response({"detail": "Unable to create epic."}, status=status.HTTP_409_CONFLICT)

        # Create User Stories to Project
        created_user_story_ids = create_user_stories(user_stories, project_id=project_id)
        logger.info(created_user_story_ids)

        # Link User Stories to Epic
        linked_user_stories = link_user_stories_to_epic(created_user_story_ids, epic_id=created_epic_id)
        logger.info(linked_user_stories)

        # Response
        response_data = {'message': 'Epic and User Stories successfully duplicated'}
        # NOTE: Re-serialize to fetch more detailed data
        response_serializer = ResponseSerializer(response_data)
        logger.info("response: %s", json.dumps(response_serializer.data, indent=4))
        return Response(response_serializer.data)
