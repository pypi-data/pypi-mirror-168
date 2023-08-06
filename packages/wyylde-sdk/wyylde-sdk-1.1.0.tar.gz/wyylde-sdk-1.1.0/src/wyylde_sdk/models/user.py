from dataclasses import dataclass
from typing import Optional

@dataclass
class UserResource:
    id: int
    blocked: bool
    nickname: str
    blacklisted: bool
    deleted: bool
    url_id: Optional[str] = None
    profile_type: Optional[int] = None
    certified: Optional[bool] = None
    online: Optional[str] = None
    tonight: Optional[bool] = None
    week_availability: Optional[bool] = None
    device: Optional[str] = None
    filtered: Optional[bool] = None
    language: Optional[str] = None
    geo_code3: Optional[str] = None
    geoposition: Optional[str] = None
    postal_address: Optional[str] = None
    main_pic: Optional[str] = None
    p0_age: Optional[int] = None
    p0_gender: Optional[str] = None
    p1_age: Optional[int] = None
    p1_gender: Optional[str] = None

    @property
    def count_people(self):
        return (self.p0_gender is not None) + (self.p1_gender is not None)

    @property
    def is_couple(self) -> bool:
        # Is a couple : there is a second user and the genders
        # of both users are different (heterosexual couple)
        return self.count_people == 2 and self.p0_gender != self.p1_gender

    @property
    def is_lady(self) -> bool:
        return self.count_people == 1 and 'woman' in (self.p0_gender, self.p1_gender)

    @property
    def is_man(self) -> bool:
        return self.count_people == 1 and 'man' in (self.p0_gender, self.p1_gender)
