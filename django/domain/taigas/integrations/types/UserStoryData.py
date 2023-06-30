from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Tag:
    name: str
    color: str

    @classmethod
    def from_list(cls, data: List[str]) -> 'Tag':
        return cls(*data)  # Unpack the list into the constructor


@dataclass
class Epic:
    id: int
    ref: int
    subject: str
    color: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Epic':
        valid_keys = set(cls.__annotations__.keys())
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)


@dataclass
class UserStory:
    id: int
    ref: int
    subject: str
    created_date: str
    modified_date: str
    tags: List[Tag]
    epics: Optional[List[Epic]]

    @classmethod
    def from_dict(cls, data: dict) -> 'UserStory':
        valid_keys = set(cls.__annotations__.keys())
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        if filtered_data.get('tags') is not None:
            filtered_data['tags'] = [Tag.from_list(tag) for tag in filtered_data['tags']]
        else:
            filtered_data['tags'] = []

        if filtered_data.get('epics') is not None:
            filtered_data['epics'] = [Epic.from_dict(epic) for epic in filtered_data['epics']]
        else:
            filtered_data['epics'] = []

        return cls(**filtered_data)
