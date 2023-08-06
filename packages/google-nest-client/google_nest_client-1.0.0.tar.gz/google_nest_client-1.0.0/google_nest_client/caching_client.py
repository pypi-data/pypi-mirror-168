from typing import List

from google_nest_client.client import GoogleNestClient
from google_nest_client.device_cache import DeviceCache


class GoogleNestCachingClient(GoogleNestClient):
    def __init__(
        self,
        project_id: str,
        device_cache: DeviceCache,
        cache_writes_enabled: bool = True,
    ):
        super().__init__(project_id)
        self.device_cache = device_cache
        self.cache_writes_enabled = cache_writes_enabled

        if self.cache_writes_enabled:
            self.device_cache.clear()
            self.load_cache()

    def load_cache(self) -> None:
        for device in super().get_devices():
            self.device_cache.upsert_device(device)

    def update_from_event(self, event: dict) -> None:
        if 'resourceUpdate' in event:
            self.device_cache.upsert_device(event['resourceUpdate'])

    def get_devices(self) -> List[dict]:
        return self.device_cache.get_devices()

    def get_device(self, device_id) -> dict:
        return self.device_cache.get_device(device_id)
