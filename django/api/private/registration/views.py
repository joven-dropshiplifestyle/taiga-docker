from typing import Any, List, Tuple, Dict

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import AccountSerializer, ExistingAccountSerializer, NewAccountSerializer

# Taiga Integration
from domain.taigas.integrations.integration_users import get_users
from domain.taigas.integrations.integration_projects import create_project
from domain.taigas.integrations.integration_roles import create_student_role, create_moderator_role
from domain.taigas.integrations.integration_members import invite_member
from domain.taigas.integrations.integration_registrations import register_user

# Taiga Database Query
from domain.taigas.queries.query_members import get_token_by_email

# Model Services
from domain.taigas.services.service_Account import create_account

# Permission
from domain.users.permissions.permission_header import HeaderKeyPermission

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import json
import logging

logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):
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
        request_body=NewAccountSerializer,
        operation_id="accounts_create",
        tags=["private.registration"],
        responses={
            200: AccountSerializer(),
            409: ExistingAccountSerializer(),
        }
    )
    def post(request: Request, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Response:
        logger.info(f"Authenticated user: {request.user}")

        # Validate Request Data
        account_serializer = NewAccountSerializer(data=request.data)
        account_serializer.is_valid(raise_exception=True)

        # Check if Taiga Username already exist
        users = get_users()
        user_exists = any(
            user.username == account_serializer.validated_data['username']
            for user in users
        )
        if user_exists:
            account_already_exist_serializer = ExistingAccountSerializer({'message': 'Username already exist'})
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

        # Get the Token Directly from Taiga Database and use in on the Registration
        member_token = get_token_by_email(email=account_serializer.validated_data['email'])
        logger.info(f"member_token {member_token}")

        # Register the User on Taiga

        # Combined First name and Last name from request Body to create a full name because Taiga only accept Full Name
        # on the registration
        first_name = account_serializer.validated_data['first_name']
        last_name = account_serializer.validated_data.get('last_name', '')

        user = register_user(
            token=member_token,
            username=account_serializer.validated_data['username'],
            email=account_serializer.validated_data['email'],
            full_name=f"{first_name} {last_name}",
            password=account_serializer.validated_data['password']
        )
        logger.info(f"registered user: {user}")

        # Save Record to Django Account Table
        account = create_account(
            username=account_serializer.validated_data['username'],
            first_name=account_serializer.validated_data['first_name'],
            # Since last name is not require on the request body we need to handle it
            last_name=account_serializer.validated_data.get('last_name', ''),
            email=account_serializer.validated_data['email'],
            password=account_serializer.validated_data['password'],
            project_id=project.id,
            project_name=project.name,
            project_slug=project.slug,
            project_description=project.description
        )

        # NOTE: Re-serialize to fetch more detailed data
        account_serializer = AccountSerializer(account)
        logger.info("response: %s", json.dumps(account_serializer.data, indent=4))
        return Response(account_serializer.data)
