from datetime import datetime
import sys
from typing import Iterable, TypeVar, Type

import requests
from dacite import from_dict, MissingValueError

from wyylde_sdk.models import (
    EventResource,
    TalkResource,
    TestimonyResource,
    UserResource,
    VisitResource,
)


T = TypeVar('T')


class Session(requests.Session):
    def __init__(self, username: str, password: str):
        self.wyylde_version = '4.1.0'
        super().__init__()
        self._authenticate(username, password)

    @property
    def now_ts(self):
        return int(datetime.now().timestamp() * 1000)

    def _authenticate(self, username: str, password: str):
        payload = {
            "login": username,
            "password": password,
            "useCookie": 0,
            "query_string": "",
            "fingerprint": "6860bbbf6298d063617a3f2f149d097d"
        }
        response = self.put(
            'https://www.wyylde.com/rest/authenticate',
            params={'version': self.wyylde_version, 'nocache': str(self.now_ts)},
            json=payload
        ).json()
        self.headers['Authorization'] = f"Bearer {response['data']['token']}"
        return

    def make_params(self, **extra):
        params = {'nocache': self.now_ts}
        params.update(extra)
        return params

    def get_generate(self, endpoint: str, klass: Type[T], params=None) -> Iterable[T]:
        params = params or {}
        params = self.make_params(**params)
        response = self.get(
            f'https://www.wyylde.com/rest/{endpoint}',
            params=params
        ).json()
        data_path = endpoint.split('/').pop()
        while response is not None:
            next_id: str = response['data']['next']
            for item in response['data'][data_path]:
                try:
                    yield from_dict(klass, item)
                except MissingValueError as e:
                    print(
                        f'Missing value from {item} : {e.field_path}',
                        file=sys.stderr
                    )
                    continue
            if next_id is not None:
                break
            response = self.get(
                f'https://www.wyylde.com/rest/{endpoint}/{next_id}',
                params=params
            ).json()


class WyyldeClient:
    def __init__(self, username: str, password: str):
        super().__init__()
        self.wyylde_version = '4.1.0'
        self.session = Session(username, password)

    @property
    def talks(self) -> Iterable[TalkResource]:
        params = {'nb': '20'}
        return self.session.get_generate('talks', TalkResource, params=params)

    def delete_talk(self, talk_id: str):
        self.session.delete(
            f'https://www.wyylde.com/rest/talks/{talk_id}',
            params={'nocache': str(self.session.now_ts)}
        )

    def post_message(self, user_id: str, message: str):
        self.session.post(
            f'https://www.wyylde.com/rest/message/send/{user_id}',
            params={'nocache': str(self.session.now_ts)},
            json={'msg': message}
        )

    def get_testimonies(self, user_id: str) -> Iterable[TestimonyResource]:
        return self.session.get_generate(
            f'profile/{user_id}/testimonies', TestimonyResource
        )

    @property
    def events(self) -> Iterable[EventResource]:
        params = {
            'version': self.wyylde_version,
            'nb': 30,
            'location': '48.85917,2.31278',
            'radius': 30
        }
        return self.session.get_generate(
            'events', EventResource, params=params
        )

    def user(self, user_id: str) -> UserResource:
        params = {
            'nocache': str(self.now_ts),
            'version': self.wyylde_version,
        }
        response = self.session.get(
            f'https://www.wyylde.com/rest/profile/{user_id}',
            params=params
        ).json()
        if response is None:
            raise Exception('User does not exist.')
        return from_dict(UserResource, response['data'])

    @property
    def visits(self) -> Iterable[VisitResource]:
        params = {
            'version': self.wyylde_version,
        }
        return self.session.get_generate(
            'my/visits', VisitResource, params=params
        )
