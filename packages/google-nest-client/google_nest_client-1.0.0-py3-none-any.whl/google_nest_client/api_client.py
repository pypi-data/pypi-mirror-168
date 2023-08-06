from typing import List
from typing import Optional

import requests
from abc import ABCMeta
from abc import abstractmethod

from google_nest_client.device import get_device_label


API_URI = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/'


class AuthenticationError(Exception):
    pass


class GoogleNestAPIClient(metaclass=ABCMeta):
    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    @abstractmethod
    def get_access_token(self) -> str:
        pass

    def api_get(self, endpoint: str) -> dict:
        resp = requests.get(
            API_URI + self.project_id + endpoint,
            headers={
                'Authorization': 'Bearer ' + self.get_access_token(),
                'Content-type': 'application/json',
            },
        )

        try:
            resp.raise_for_status()
        except requests.HTTPError as ex:
            if ex.response.status_code in (401, 403):
                raise AuthenticationError

        return resp.json()

    def api_post(self, endpoint: str, json: Optional[dict] = None) -> dict:
        resp = requests.post(
            API_URI + self.project_id + endpoint,
            headers={
                'Authorization': 'Bearer ' + self.get_access_token(),
                'Content-type': 'application/json',
            },
            json=json,
        )

        try:
            resp.raise_for_status()
        except requests.HTTPError as ex:
            if ex.response.status_code in (401, 403):
                raise AuthenticationError

        return resp.json()

    def get_structures(self) -> dict:
        return self.api_get(
            '/structures'
        )['structures']

    def get_devices(self) -> List[dict]:
        return self.api_get(
            '/devices'
        )['devices']

    def get_device(self, device_id: str) -> dict:
        return self.api_get('/devices/' + device_id)

    def get_devices_by_type(self, device_type):
        return [
            device for device in self.get_devices()
            if device['type'] == device_type
        ]

    def get_devices_by_type_and_label(
        self,
        device_type: str,
        label: str
    ) -> List[dict]:
        return [
            device for device in self.get_devices_by_type(device_type)
            if get_device_label(device) == label
        ]

    def execute_command(
        self,
        device_id: str,
        command: str,
        params: str
    ) -> dict:
        return self.api_post(
            '/devices/' + device_id + ':executeCommand',
            json={
                'command': command,
                'params': params,
            },
        )
