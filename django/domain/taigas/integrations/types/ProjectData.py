from dataclasses import dataclass


@dataclass
class Project:
    id: int
    name: str
    slug: str
    description: str
    created_date: str
    modified_date: str
    creation_template: int

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)
