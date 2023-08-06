from typing import Iterable

import time
from abc import ABCMeta
from abc import abstractmethod

from google_nest_client.device import get_device_id


class DeviceCache(metaclass=ABCMeta):
    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def upsert_device(self, device_update: dict) -> None:
        pass

    def get_devices(self) -> Iterable[dict]:
        pass

    def get_device(self, device_id: str) -> dict:
        pass


class InMemoryDeviceCache(DeviceCache):
    def __init__(self) -> None:
        self.id_to_device: dict = {}

    def clear(self) -> None:
        self.id_to_device = {}

    def upsert_device(self, device_update: dict) -> None:
        device_id = get_device_id(device_update)
        device = self.id_to_device.get(device_id)

        if not device:
            self.id_to_device[device_id] = device_update
            return

        if 'traits' in device_update:
            for k, v in device_update['traits']:
                device['traits'][k] = v

        if 'events' in device_update:
            for k, v in device_update['events']:
                device['events'][k] = v
                device['events'][k]['timestamp'] = int(time.time())

    def get_devices(self) -> Iterable[dict]:
        return self.id_to_device.values()

    def get_device(self, device_id: str) -> dict:
        return self.id_to_device[device_id]
