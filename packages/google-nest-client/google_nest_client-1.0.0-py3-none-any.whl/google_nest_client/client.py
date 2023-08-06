from typing import List
from typing import Optional

from google_nest_client.api_client import GoogleNestAPIClient
from google_nest_client.camera import Camera
from google_nest_client.thermostat import Thermostat


class GoogleNestClient(GoogleNestAPIClient):
    def get_cameras(self) -> List[Camera]:
        return [
            Camera(self, device)
            for device in self.get_devices_by_type('sdm.devices.types.CAMERA')
        ]

    def get_thermostats(self) -> List[Thermostat]:
        return [
            Thermostat(self, device)
            for device in self.get_devices_by_type('sdm.devices.types.THERMOSTAT')
        ]

    def get_camera(self, device_id: str) -> Camera:
        return Camera(self, self.get_device(device_id))

    def get_thermostat(self, device_id: Optional[str] = None) -> Thermostat:
        if device_id:
            return Thermostat(self, self.get_device(device_id))
        else:
            device_dicts = self.get_devices_by_type('sdm.devices.types.THERMOSTAT')
            return Thermostat(self, device_dicts[0])

    def get_camera_by_label(self, label: str) -> Optional[Camera]:
        matched_devices = self.get_devices_by_type_and_label(
            'sdm.devices.types.CAMERA',
            label,
        )

        if matched_devices:
            return Camera(self, matched_devices[0])
        else:
            return None

    def get_thermostat_by_label(self, label: str = 'Thermostat') -> Optional[Thermostat]:
        matched_devices = self.get_devices_by_type_and_label(
            'sdm.devices.types.THERMOSTAT',
            label,
        )

        if matched_devices:
            return Thermostat(self, matched_devices[0])
        else:
            return None
