from typing import List, Optional
from dataclasses import dataclass


@dataclass
class User:
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

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)
