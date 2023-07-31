# DRF
from typing import Optional
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

# Serializers
from .serializers import ReadAccountSerializer

# Services
from domain.taigas.services.service_Account import get_account_by_email

# Permission
from domain.users.permissions.permission_header import HeaderKeyPermission

# Taiga DB Queries
from domain.taigas.queries.query_members import check_email_exists

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import logging
logger = logging.getLogger(__name__)


class AccountEmailAPIView(APIView):

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
        responses={
            200: ReadAccountSerializer()
        },
        operation_description="Get account details by email",
        operation_id="account_read_by_email",
        tags=["private.accounts"],
    )
    def get(request: Request, email_id: Optional[str] = None) -> Response:
        logger.info(f"authenticated: {request.user}")
        account = get_account_by_email(email_id)

        # This means the Student is not yet existing on our Taiga User Database
        if account is None:
            data = {"message": "User not found."}
            return Response({"success": False, "data": data})

        # We are returning this because we want the Student be able to create a new Taiga Project
        # because even though he already had an account his project is already deleted.
        has_active_project = check_email_exists(email_id)
        if not has_active_project:
            data = {"message": "User exist but has no active Taiga Project"}
            return Response({"success": False, "data": data})

        account_serializer = ReadAccountSerializer(account)
        return Response(account_serializer.data)
