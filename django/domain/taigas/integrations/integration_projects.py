import os
import requests
import logging

from .integration_auth import fetch_root_auth_data
from .types.ProjectData import Project

logger = logging.getLogger(__name__)


def create_project(project_name: str, project_description: str) -> Project:

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/projects'
    url = f"{base_url}{endpoint}"
    data = {
        "name": project_name,
        "description": project_description,
        "is_private": True,
        "creation_template": os.environ.get('TAIGA_PROJECT_TEMPLATE', '2')
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    if response.status_code == 201:
        response_json = response.json()
        project_data = Project.from_dict(response_json)
        logger.info(response_json)
        return project_data
    else:
        logger.error(f"Failed to create project, status code: {response.status_code}")
        raise Exception("Failed to create project")
