from dataclasses import dataclass
from typing import Optional


@dataclass
class TestimonyResource:
    id: int
    url_id: str
    date: int
    text: str
    profile_type: str
    nickname: str
    picture: Optional[str] = None
