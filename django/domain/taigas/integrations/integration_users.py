import os
import requests
import logging
from typing import List

from .integration_auth import fetch_auth_data
from .types.UserData import User

logger = logging.getLogger(__name__)


def get_users() -> List[User]:

    auth_data = fetch_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/users'
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        users = [User.from_dict(user_data) for user_data in response_json]
        logger.info(response_json)
        return users
    else:
        logger.error(f"Failed to fetch user data, status code: {response.status_code}")
        raise Exception("Failed to fetch user data")
