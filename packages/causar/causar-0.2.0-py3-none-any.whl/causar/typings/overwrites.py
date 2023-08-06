from typing import TypedDict


class PermissionsOverwrite(TypedDict):
    id: str
    type: int
    allow: str
    deny: str
