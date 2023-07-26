from typing import Any, Tuple, Dict

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Serializers
from .serializers import AccountSerializer, ExistingAccountSerializer, NewAccountSerializer

# Taiga Integration
from domain.taigas.integrations.integration_users import get_users
from domain.taigas.integrations.integration_projects import duplicate_template_project
from domain.taigas.integrations.integration_roles import create_student_role, create_moderator_role
from domain.taigas.integrations.integration_members import invite_member, get_template_users_id
from domain.taigas.integrations.integration_registrations import register_user
from domain.taigas.integrations.integration_userstories import create_user_story

# Taiga Database Query
from domain.taigas.queries.query_members import get_token_by_email

# Model Services
from domain.taigas.services.service_Account import create_account, get_account_by_email

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

        # Check if already created based on our Django Account Model
        account = get_account_by_email(account_serializer.validated_data['email'])
        # If Existing we don't have to create the Taiga Project, we just have to create the task
        # Reason: because the Student might send the form twice, and we wanted to avoid duplicated projects
        if account:
            account_already_exist_serializer = ExistingAccountSerializer({
                'message': 'This Email had an existing Taiga Project.'
            })
            return Response(
                account_already_exist_serializer.data,
                status=status.HTTP_409_CONFLICT
            )

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

        # Get Template Project Users ID's
        users_id = get_template_users_id()

        # Duplicate Project
        project = duplicate_template_project(
            project_name=account_serializer.validated_data['project_name'],
            project_description=account_serializer.validated_data['project_description'],
            users_id=users_id
        )

        # "Member" is the Student default Role
        role_id = None
        for role in project.roles:
            if role.name == "Member":
                role_id = role.id
                logger.info(f"role_id: {role_id}")

        # As per Taiga Docs: username (required): user username or email
        student_member = invite_member(
            project_id=project.id,
            role_id=role_id,
            username=account_serializer.validated_data['email']
        )

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

        # Create the Initial User Story if it's provided on the request
        if account_serializer.validated_data.get('task_title', ''):
            created_user_story_id = create_user_story(
                subject=account_serializer.validated_data['task_title'],
                description=account_serializer.validated_data.get('task_content', ''),
                project_id=project.id
            )
            logger.info(f"user story created with id: {created_user_story_id}")

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
