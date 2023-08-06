from dataclasses import dataclass

from .user import UserResource


@dataclass
class VisitResource:
    id: str
    new: bool
    sender: UserResource
    ts: int
