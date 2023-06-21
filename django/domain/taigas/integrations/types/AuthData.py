from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Auth:
    id: int
    username: str
    full_name: str
    full_name_display: str
    color: str
    bio: str
    lang: str
    theme: str
    timezone: str
    is_active: bool
    photo: Optional[str]
    big_photo: Optional[str]
    gravatar_id: str
    roles: List[str]
    total_private_projects: int
    total_public_projects: int
    email: str
    uuid: str
    date_joined: str
    read_new_terms: bool
    accepted_terms: bool
    max_private_projects: Optional[int]
    max_public_projects: Optional[int]
    max_memberships_private_projects: Optional[int]
    max_memberships_public_projects: Optional[int]
    verified_email: bool
    refresh: str
    auth_token: str

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)
