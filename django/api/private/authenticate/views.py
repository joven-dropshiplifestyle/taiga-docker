from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
from .serializers import AuthenticationSerializer, AuthenticationResponseSerializer

# Taiga Integration
from domain.taigas.integrations.integration_auth import fetch_auth_data


# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import json
import logging
logger = logging.getLogger(__name__)


class AuthenticateAPIView(APIView):

    @staticmethod
    @swagger_auto_schema(
        request_body=AuthenticationSerializer,
        operation_id="authenticate",
        tags=["private"],
        responses={
            200: AuthenticationResponseSerializer()
        }
    )
    def post(request, *args, **kwargs):
        logger.info(f"authenticated: {request.user}")

        # Validate Request Data
        auth_credential_serializer = AuthenticationSerializer(data=request.data)
        auth_credential_serializer.is_valid(raise_exception=True)

        auth_data = fetch_auth_data(
            auth_credential_serializer.validated_data['email'],
            auth_credential_serializer.validated_data['password']
        )

        auth_credential_serializer = AuthenticationResponseSerializer({
            'token': auth_data.auth_token,
            'refresh': auth_data.refresh,
            'user_info': auth_data
        })

        return Response(auth_credential_serializer.data)
