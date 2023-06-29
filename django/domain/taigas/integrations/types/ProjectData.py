from dataclasses import dataclass
from typing import List


@dataclass
class Role:
    id: int
    name: str
    slug: str
    permissions: List[str]
    order: int
    computable: bool
    project_id: int

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)


@dataclass
class Project:
    id: int
    name: str
    slug: str
    description: str
    created_date: str
    modified_date: str
    roles: List[Role]

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys

        roles = filtered_data.get('roles', [])
        filtered_data['roles'] = [Role.from_dict(role) for role in roles]
        return cls(**filtered_data)
