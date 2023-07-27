import os
import requests
import logging
from typing import Dict
from .integration_auth import fetch_root_auth_data

logger = logging.getLogger(__name__)


def create_wiki(auth_token: str, content: str, project_id: int) -> Dict[str, any]:

    base_url = os.environ.get('TAIGA_ENDPOINT', '')
    endpoint = "/wiki"
    url = f"{base_url}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    data = {
        "project": project_id,
        "slug": 'home',
        "content": content
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        wiki_data = response.json()
        logger.info(f"Wiki created successfully, ID: {wiki_data['id']}")
        return wiki_data
    else:
        logger.error(f"Failed to create wiki, status code: {response.status_code}")
        raise Exception("Failed to create the wiki")
