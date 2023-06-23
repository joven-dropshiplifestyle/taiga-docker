import requests
import logging
import os

from .integration_auth import fetch_auth_data
from .types.MemberData import Member

logger = logging.getLogger(__name__)


def invite_member(project_id: int, role_id: int, username: str) -> Member:

    auth_data = fetch_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f'/memberships'
    url = f"{base_url}{endpoint}"
    data = {
        "project": project_id,
        "role": role_id,
        "username": username
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 201:
        response_json = response.json()
        member_data = Member.from_dict(response_json)
        logger.info(response_json)
        return member_data
    else:
        logger.error(f"Failed to invite member, status code: {response.status_code}")
        raise Exception("Failed to invite member")
