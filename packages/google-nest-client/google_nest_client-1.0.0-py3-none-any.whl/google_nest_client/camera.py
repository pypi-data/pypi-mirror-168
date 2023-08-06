from google_nest_client.device import Device


class Camera(Device):
    def get_last_motion_event(self) -> dict:
        return self.get_event('CameraMotion.Motion')

    def get_last_person_event(self) -> dict:
        return self.get_event('CameraPerson.Person')

    def get_last_sound_event(self) -> dict:
        return self.get_event('CameraSound.Sound')

    def generate_image(self, event_id: str) -> dict:
        return self.api_client.execute_command(
            self.device_id,
            'sdm.devices.commands.CameraEventImage.GenerateImage',
            {'eventId': event_id},
        )
