from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import QuerySerializer, ReadAuthCredentialSerializer

# Taiga Integration
from domain.taigas.integrations.integration_auth import fetch_auth_data


# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import json
import logging
logger = logging.getLogger(__name__)


class AuthenticateAPIView(APIView):

    # permission_classes = (IsAuthenticated,)

    @staticmethod
    @swagger_auto_schema(
        query_serializer=QuerySerializer(),
        operation_id="authenticate",
        tags=["private.authenticate"],
        responses={
            200: ReadAuthCredentialSerializer()
        }
    )
    def get(request, *args, **kwargs):
        logger.info(f"authenticated: {request.user}")

        auth_data = fetch_auth_data()
        auth_credential_serializer = ReadAuthCredentialSerializer({
            'token': auth_data.auth_token,
            'refresh': auth_data.refresh,
            'user_info': auth_data
        })

        return Response(auth_credential_serializer.data)
