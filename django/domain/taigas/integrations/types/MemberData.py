from dataclasses import dataclass


@dataclass
class Member:
    id: int
    project: int
    role: int
    is_admin: bool
    created_at: str
    user_order: int
    role_name: str
    project_name: str
    project_slug: str
    email: str

    @classmethod
    def from_dict(cls, data: dict):
        valid_keys = set(cls.__annotations__.keys())  # Get the valid attribute names
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}  # Filter out unexpected keys
        return cls(**filtered_data)
