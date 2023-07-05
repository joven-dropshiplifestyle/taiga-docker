import os
import requests
import logging

from typing import List
from .integration_auth import fetch_root_auth_data
from .types.ProjectData import Project

logger = logging.getLogger(__name__)


def get_all_projects() -> List[Project]:
    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/projects'
    url = f"{base_url}{endpoint}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        projects_data = [Project.from_dict(project) for project in response_json]
        logger.info(response_json)
        return projects_data
    else:
        logger.error(f"Failed to retrieve projects, status code: {response.status_code}")
        raise Exception("Failed to retrieve projects")


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


def duplicate_template_project(project_name: str, project_description: str, users_id: List[int]) -> Project:

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    project_template_id = os.environ.get('TAIGA_PROJECT_TEMPLATE', '2')
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f"/projects/{project_template_id}/duplicate"
    url = f"{base_url}{endpoint}"

    # Skip None and User ID of the Owner of the Token Credentials (Because he is automatically added)
    users = [{"id": user_id} for user_id in users_id if user_id is not None and user_id != auth_data.id]

    data = {
        "name": project_name,
        "description": project_description,
        "is_private": True,
        "users": users
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


def get_project_id_by_slug(slug: str) -> int:
    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = "/projects/by_slug"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    params = {
        "slug": slug
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        project_id = response.json()['id']
        logger.info(f"Project ID retrieved successfully, ID: {project_id}")
        return project_id
    else:
        logger.error(f"Failed to retrieve project ID, status code: {response.status_code}")
        raise Exception("Failed to retrieve project ID")
