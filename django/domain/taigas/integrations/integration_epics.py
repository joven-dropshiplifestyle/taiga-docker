import os
import requests
import logging

from .integration_auth import fetch_root_auth_data
from .types.UserStoryData import UserStory

logger = logging.getLogger(__name__)


def create_epic(user_story: UserStory, project_id: int) -> int:
    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = "/epics"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    data = {
        "project": project_id,
        "subject": user_story.epics[0].subject,
        "color": user_story.epics[0].color
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        epic_id = response.json()['id']
        logger.info(f"Epic created successfully, ID: {epic_id}")
        return epic_id
    else:
        logger.error(f"Failed to create epic, status code: {response.status_code}")
        raise Exception("Failed to create epic")
