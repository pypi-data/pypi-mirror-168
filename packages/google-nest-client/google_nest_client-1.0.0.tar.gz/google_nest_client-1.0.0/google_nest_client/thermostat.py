from google_nest_client.device import Device


class Thermostat(Device):
    def get_hvac_status(self) -> str:
        return self.get_trait('ThermostatHvac')['status']

    def get_mode(self) -> str:
        return self.get_trait('ThermostatMode')['mode']

    def get_ambient_temperature(self) -> float:
        deg_c = self.get_trait('Temperature')['ambientTemperatureCelsius']
        return celsius_to_farenheit(deg_c)

    def get_heating_temperature(self) -> float:
        deg_c = self.get_trait('ThermostatTemperatureSetpoint')['heatCelsius']
        return celsius_to_farenheit(deg_c)

    def get_ambient_humidity(self) -> float:
        return self.get_trait('Humidity')['ambientHumidityPercent']

    def set_heat(self, deg_f: float) -> None:
        self.api_client.execute_command(
            self.device_id,
            'sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat',
            {'heatCelsius': farenheit_to_celsius(deg_f)},
        )


def farenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def celsius_to_farenheit(c):
    return c * 9 / 5 + 32
