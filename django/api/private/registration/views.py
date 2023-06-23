from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import ReadAccountSerializer, AccountAlreadyExistSerializer, CreateAccountSerializer

# Taiga Integration
from domain.taigas.integrations.integration_users import get_users
from domain.taigas.integrations.integration_projects import create_project
from domain.taigas.integrations.integration_roles import create_student_role, create_moderator_role
from domain.taigas.integrations.integration_members import invite_member

# Model Services
from domain.taigas.services.service_Account import create_account

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import json
import logging
logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    @swagger_auto_schema(
        request_body=CreateAccountSerializer,
        operation_id="accounts_create",
        tags=["private.registration"],
        responses={
            200: ReadAccountSerializer(),
            409: AccountAlreadyExistSerializer(),
        }
    )
    def post(request, *args, **kwargs):
        logger.info(f"authenticated: {request.user}")

        # Validate Request Data
        account_serializer = CreateAccountSerializer(data=request.data)
        account_serializer.is_valid(raise_exception=True)

        # Check if Taiga Username already exist
        users = get_users()
        user_exists = any(
            user.username == account_serializer.validated_data['username']
            for user in users
        )
        if user_exists:
            account_already_exist_serializer = AccountAlreadyExistSerializer({'message': 'Username already exist'})
            return Response(
                account_already_exist_serializer.data,
                status=status.HTTP_409_CONFLICT
            )

        # Create New Project
        project = create_project(
            project_name=account_serializer.validated_data['project_name'],
            project_description=account_serializer.validated_data['project_description']
        )

        # Create the Student and Moderator Role
        student_role = create_student_role(project.id)
        moderator_role = create_moderator_role(project.id)

        # As per Taiga Docs: username (required): user username or email
        student_member = invite_member(
            project_id=project.id,
            role_id=student_role.id,
            username=account_serializer.validated_data['email']
        )

        # TODO: Invite Bulk Members of Admin
        # Moderator should already existed on Taiga
        # List of Moderator ID
        # moderator_members = bulk_invite_member(moderator_ids,  moderator_role.id, project.id)

        # TODO: Access Database to get the Invitation Code
        # TODO: Based on the Invitation code automate the registration

        account = create_account(
            username=account_serializer.validated_data['username'],
            email=account_serializer.validated_data['email'],
            password=account_serializer.validated_data['password'],
            project_id=project.id,
            project_name=project.name,
            project_slug=project.slug,
            project_description=project.description
        )

        # NOTE: Re-serialize to fetch more detailed data
        account_serializer = ReadAccountSerializer(account)
        logger.info("response: %s", json.dumps(account_serializer.data, indent=4))
        return Response(account_serializer.data)
