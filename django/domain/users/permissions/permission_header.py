import os
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed


class HeaderKeyPermission(permissions.BasePermission):
    """
    Global permission to check for a key in the header
    """

    def has_permission(self, request, view):
        header_key = request.headers.get('X-SPECIAL-KEY')
        secret_key = os.getenv('X_SPECIAL_KEY', default=None)

        if not header_key or header_key != secret_key:
            raise AuthenticationFailed('No key found in headers or key is not correct')

        return True
