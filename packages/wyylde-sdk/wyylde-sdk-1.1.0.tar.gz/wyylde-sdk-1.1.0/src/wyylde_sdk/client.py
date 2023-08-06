from datetime import datetime
import sys
from typing import Any, Iterable, Optional, TypeVar, Type

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
    def now_ts(self) -> str:
        '''
        Property that returns the current timestamp as a string.

        :return: Current timestamp
        :rtype: str
        '''
        return str(int(datetime.now().timestamp() * 1000))

    def _authenticate(self, username: str, password: str) -> None:
        '''
        Function that performs the authentication to wyylde using the provided username/password
        Sets the Authorization header of the session.

        :param username: Wyylde username
        :type username: str
        :param password: Wyylde password
        :type password: str
        '''
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

    def make_params(self, **extra) -> dict[str, Any]:
        '''
        Helper function that injects the 'nocache' URI param into the parameters.

        :return: New params dictionary
        :rtype: dict[str, Any]
        '''
        params = {'nocache': self.now_ts}
        params.update(extra)
        return params

    def get_generate(
        self, endpoint: str, klass: Type[T], params: Optional[dict[str, Any]]=None
    ) -> Iterable[T]:
        '''
        Generator function that yields elements of an array as their corresponding models.

        :param endpoint: Endpoint of the Wyylde API to call
        :type endpoint: str
        :param klass: The model to cast the objects as
        :type klass: Type[T]
        :param params: Additional URI params to pass on, nocache is set by default, defaults to None
        :type params: Optional[dict[str, Any]], optional
        :return: None
        :rtype: Iterable[T]
        :yield: Iterator of objects of type T as returned by the API.
        :rtype: Iterator[Iterable[T]]
        '''
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
            'version': self.session.wyylde_version,
            'nb': 30,
            'location': '48.85917,2.31278',
            'radius': 30
        }
        return self.session.get_generate(
            'events', EventResource, params=params
        )

    def user(self, user_id: str) -> UserResource:
        params = {
            'nocache': self.session.now_ts,
            'version': self.session.wyylde_version,
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
            'version': self.session.wyylde_version,
        }
        return self.session.get_generate(
            'my/visits', VisitResource, params=params
        )
