from dataclasses import dataclass
from typing import Optional

from .user import UserResource


@dataclass
class TalkResource:
    url_id: str
    user: UserResource
    id: str
    msg_id: str
    msg_urlid: str
    read:Optional[bool] = None
    reply: Optional[bool] = None
    date: Optional[int] = None
    sample: Optional[str] = None
    msg_sample: Optional[str] = None
    msg_last: Optional[int] = None
    format: Optional[str] = None
    deny_write: Optional[str] = None
    match_seeks: Optional[bool] = None
