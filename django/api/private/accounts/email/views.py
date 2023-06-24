# DRF
from typing import Optional
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import ReadAccountSerializer

# Services
from domain.taigas.services.service_Account import get_account_by_email

# Permission
from domain.users.permissions.permission_header import HeaderKeyPermission

# Django Shortcuts
from django.http import Http404

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
        if account is None:
            raise Http404
        account_serializer = ReadAccountSerializer(account)
        return Response(account_serializer.data)
