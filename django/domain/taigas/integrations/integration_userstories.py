import os
import requests
import logging
from typing import List

from .integration_auth import fetch_root_auth_data
from .types.UserStoryData import UserStory

logger = logging.getLogger(__name__)


def get_user_stories_by_epic_from_template_project(epic_id: str) -> List[UserStory]:

    project_template_id = os.environ.get('TAIGA_PROJECT_TEMPLATE', '2')

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f"/userstories?project={project_template_id}"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        user_stories = [
            UserStory.from_dict(story_data)
            for story_data in response_json
            if story_data['epics'] is not None  # First check if 'epics' is not None
            and any(epic.id == int(epic_id) for epic in UserStory.from_dict(story_data).epics)
        ]
        logger.info(response_json)
        return user_stories
    else:
        logger.error(f"Failed to fetch user stories, status code: {response.status_code}")
        raise Exception("Failed to fetch user stories")


def create_user_stories(user_stories: List[UserStory], project_id: int) -> List[int]:

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = "/userstories"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    created_user_story_ids = []

    for user_story in user_stories:
        data = {
            "project": project_id,
            "subject": user_story.subject,
            "tags": [[tag.name, tag.color] for tag in user_story.tags]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            user_story_id = response.json()['id']
            logger.info(f"User story created successfully, ID: {user_story_id}")
            created_user_story_ids.append(user_story_id)
        else:
            logger.error(f"Failed to create user story, status code: {response.status_code}")

    if not created_user_story_ids:
        raise Exception("Failed to create any user stories")

    return created_user_story_ids


def link_user_stories_to_epic(user_stories_ids: List[int], epic_id: int) -> List[int]:

    auth_data = fetch_root_auth_data()
    auth_token = auth_data.auth_token
    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = f"/epics/{epic_id}/related_userstories"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    linked_user_story_ids = []

    for user_story_id in user_stories_ids:
        data = {
            "epic": epic_id,
            "user_story": user_story_id
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            linked_user_story_id = response.json()['user_story']
            logger.info(f"User story ID: {linked_user_story_id} linked to epic ID: {epic_id} successfully")
            linked_user_story_ids.append(linked_user_story_id)
        else:
            logger.error(f"Failed to link user story ID: {user_story_id} to epic ID: {epic_id}, status code: {response.status_code}")

    if not linked_user_story_ids:
        raise Exception("Failed to link any user stories to the epic")

    return linked_user_story_ids
