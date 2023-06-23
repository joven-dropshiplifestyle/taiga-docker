import os
import requests
import json
import logging
from .types.AuthData import Auth

from typing import Union
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


def fetch_root_auth_data() -> Auth:
    base_url = os.environ.get('TAIGA_ENDPOINT', 'http://taiga-back:8000/api/v1')
    endpoint = '/auth'
    url = f"{base_url}{endpoint}"

    headers = {'Content-Type': 'application/json'}
    data = {
        "username": os.environ.get('TAIGA_SUPER_ADMIN_USERNAME', ''),
        "password": os.environ.get('TAIGA_SUPER_ADMIN_PASSWORD', ''),
        "type": os.environ.get('TAIGA_SUPER_ADMIN_TYPE', ''),
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        auth_data = Auth.from_dict(response_json)
        logger.info(response_json)
        return auth_data
    else:
        logger.error(f"Failed to fetch data, status code: {response.status_code}")
        raise APIException("Failed to fetch authentication data")


def fetch_auth_data(email: str, password: str) -> Union[Auth, APIException]:
    base_url = os.environ.get('TAIGA_ENDPOINT', 'http://taiga-back:8000/api/v1')
    endpoint = '/auth'
    url = f"{base_url}{endpoint}"

    headers = {'Content-Type': 'application/json'}
    data = {
        "username": email,
        "password": password,
        "type": 'normal',
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        auth_data = Auth.from_dict(response_json)
        logger.info(response_json)
        return auth_data
    else:
        logger.error(f"Failed to fetch data, status code: {response.status_code}")
        raise APIException("Failed to fetch authentication data")
