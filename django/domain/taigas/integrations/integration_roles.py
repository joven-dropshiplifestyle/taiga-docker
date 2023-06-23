import requests
import logging

import json
import os

from .integration_auth import fetch_auth_data
from .types.RoleData import Role

logger = logging.getLogger(__name__)


def create_student_role(project_id: int) -> Role:
    auth_data = fetch_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/roles'
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    data = {
        "name": "Student",
        "order": 70,
        "permissions": [
            "comment_us",
            "view_us",
            "view_project"
        ],
        "project": project_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        response_json = response.json()
        role_data = Role.from_dict(response_json)
        logger.info(f"Role created successfully: {response_json}")
        return role_data
    else:
        logger.error(f"Failed to create role, status code: {response.status_code}")
        raise Exception("Failed to create role")


def create_moderator_role(project_id: int) -> Role:
    auth_data = fetch_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = '/roles'
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    data = {
        "name": "Moderator",
        "order": 80,
        "permissions": [
            "add_issue",
            "modify_issue",
            "delete_issue",
            "view_issues",
            "add_milestone",
            "modify_milestone",
            "delete_milestone",
            "view_milestones",
            "view_project",
            "add_task",
            "modify_task",
            "delete_task",
            "view_tasks",
            "add_us",
            "modify_us",
            "delete_us",
            "view_us",
            "add_wiki_page",
            "modify_wiki_page",
            "delete_wiki_page",
            "view_wiki_pages",
            "add_wiki_link",
            "delete_wiki_link",
            "view_wiki_links",
            "view_epics",
            "add_epic",
            "modify_epic",
            "delete_epic",
            "comment_epic",
            "comment_us",
            "comment_task",
            "comment_issue",
            "comment_wiki_page"
        ],
        "project": project_id
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        response_json = response.json()
        role_data = Role.from_dict(response_json)
        logger.info(f"Role created successfully: {response_json}")
        return role_data
    else:
        logger.error(f"Failed to create role, status code: {response.status_code}")
        raise Exception("Failed to create role")
