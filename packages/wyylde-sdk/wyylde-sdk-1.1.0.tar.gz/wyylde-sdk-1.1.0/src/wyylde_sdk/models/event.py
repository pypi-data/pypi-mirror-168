from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EventOwnerResource:
    id: str
    type: str
    name: str
    status: Optional[str] = None
    pic: Optional[str] = None


@dataclass
class EventPricingResource:
    man: Optional[int]
    woman: Optional[int]
    couple: Optional[int]


@dataclass
class EventResource:
    id: str
    url_id: str
    title: str
    date: Optional[str]
    type: Optional[int]
    location_short: Optional[str]
    restriction: Optional[bool]
    category: Optional[str]
    debug_status: Optional[str]
    debug_create: Optional[str]
    flyer: Optional[str]
    flyer_thumb: Optional[str]
    owner: EventOwnerResource
    location_code3: Optional[str]
    location_area3: Optional[str]
    nb_users: Optional[int]
    pricing: Any
