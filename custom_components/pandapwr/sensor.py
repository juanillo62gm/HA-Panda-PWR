"""Sensor platform for PandaPWR integration in Home Assistant."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
)

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform for PandaPWR."""
    api = hass.data[DOMAIN][entry.entry_id]
    device_id = f"pandapwr_{entry.data['ip_address']}"
    async_add_entities(
        [
            CountdownStateSensor(api, entry, device_id),
            AutoPoweroffSensor(api, entry, device_id),
            CountdownSensor(api, entry, device_id),
            VoltageSensor(api, entry, device_id),
            CurrentSensor(api, entry, device_id),
            PowerSensor(api, entry, device_id),
            EnergyUsageSensor(api, entry, device_id),
        ],
        True,
    )


class PandaPWRSensor(SensorEntity):
    """Base class for PandaPWR sensors."""

    def __init__(
        self,
        api,
        entry,
        device_id,
        name,
        unique_id_suffix,
        native_unit_of_measurement=None,
        device_class=None,
    ):
        """Initialize the sensor with common attributes."""
        self._api = api
        self._entry = entry
        self._attr_name = name
        self._attr_unique_id = f"{device_id}_{unique_id_suffix}"
        self._attr_native_value = None
        self._attr_native_unit_of_measurement = native_unit_of_measurement
        self._attr_device_class = device_class
        self._device_id = device_id

    async def async_update(self):
        """Fetch latest state data from the device."""
        data = await self._api.get_data()
        self.process_data(data)

    @property
    def device_info(self):
        """Return device information to group in the UI."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Panda PWR",
            "manufacturer": "Panda",
            "model": "PWR Device",
            "sw_version": "1.0",
        }

    def process_data(self, data):
        """Process data received from the API."""
        raise NotImplementedError


class CountdownStateSensor(PandaPWRSensor):
    """Sensor for monitoring countdown state on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Countdown State", "countdown_state")

    def process_data(self, data):
        """Process countdown state data from the API."""
        self._attr_native_value = data.get("countdown_state")


class AutoPoweroffSensor(PandaPWRSensor):
    """Sensor for monitoring auto power-off state on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Auto Poweroff", "auto_poweroff")

    def process_data(self, data):
        """Process auto power-off data from the API."""
        self._attr_native_value = data.get("auto_poweroff")


class CountdownSensor(PandaPWRSensor):
    """Sensor for monitoring countdown timer on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Countdown", "countdown", "s")

    def process_data(self, data):
        """Process countdown timer data from the API."""
        self._attr_native_value = data.get("countdown")


class VoltageSensor(PandaPWRSensor):
    """Sensor for monitoring voltage on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(
            api,
            entry,
            device_id,
            "Voltage",
            "voltage",
            UnitOfElectricPotential.VOLT,
            "voltage",
        )

    def process_data(self, data):
        """Process voltage data from the API."""
        self._attr_native_value = data.get("voltage") or 0.0


class CurrentSensor(PandaPWRSensor):
    """Sensor for monitoring current on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(
            api,
            entry,
            device_id,
            "Current",
            "current",
            UnitOfElectricCurrent.AMPERE,
            "current",
        )

    def process_data(self, data):
        """Process current data from the API."""
        self._attr_native_value = data.get("current") or 0.0


class PowerSensor(PandaPWRSensor):
    """Sensor for monitoring power on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(
            api, entry, device_id, "Power", "power", UnitOfPower.WATT, "power"
        )

    def process_data(self, data):
        """Process power data from the API."""
        self._attr_native_value = data.get("power") or 0.0


class EnergyUsageSensor(PandaPWRSensor):
    """Sensor for monitoring energy usage on a PandaPWR device."""

    def __init__(self, api, entry, device_id):
        super().__init__(
            api,
            entry,
            device_id,
            "Energy Usage",
            "energy_usage",
            UnitOfEnergy.KILO_WATT_HOUR,
            "energy",
        )

    def process_data(self, data):
        """Process energy usage data from the API."""
        self._attr_native_value = data.get("ele") or 0.0
