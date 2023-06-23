from dataclasses import dataclass
from typing import List


@dataclass
class Role:
    id: int
    name: str
    slug: str
    project: int
    order: int
    computable: bool
    permissions: List[str]
    members_count: int

    @classmethod
    def from_dict(cls, data: dict) -> 'Role':
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)
