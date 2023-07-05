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


def get_epic_id_from_project_template_by_ref_id(ref_id: int) -> int:

    project_template_id = os.environ.get('TAIGA_PROJECT_TEMPLATE', '2')

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f"/epics/by_ref"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    params = {
        "ref": ref_id,
        "project": project_template_id
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        epic_id = response.json()['id']
        logger.info(f"Epic ID retrieved successfully, ID: {epic_id}")
        return epic_id
    else:
        logger.error(f"Failed to retrieve epic ID, status code: {response.status_code}")
        raise Exception("Failed to retrieve epic ID")


def get_epics_from_project_template():

    project_template_id = os.environ.get('TAIGA_PROJECT_TEMPLATE', '2')

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f"/epics?project={project_template_id}"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        epics = response.json()
        logger.info(f"Successfully retrieved {len(epics)} epics for project ID: {project_template_id}")
        return epics
    else:
        logger.error(f"Failed to retrieve epics, status code: {response.status_code}")
        raise Exception("Failed to retrieve epics")
