import os
import requests
import logging
import json
from .integration_auth import fetch_root_auth_data

from .types.UserData import User

logger = logging.getLogger(__name__)


def register_user(
        token: str,
        username: str,
        full_name: str,
        email: str,
        password: str
) -> User:
    user_data = {
        "token": token,
        "accepted_terms": True,
        "username": username,
        "full_name": full_name,
        "email": email,
        "password": password,
        "type": "private",
        "existing": False
    }

    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/auth/register'
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(user_data))

    if response.status_code == 201:
        response_json = response.json()
        user = User.from_dict(response_json)
        logger.info(response_json)
        return user
    else:
        logger.error(f"Failed to register user, status code: {response.status_code}")
        raise Exception("Failed to register user")
