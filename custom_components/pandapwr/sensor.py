from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfPower,
    UnitOfEnergy,
)
from homeassistant.helpers.entity import EntityCategory
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
    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Countdown State", "countdown_state")

    def process_data(self, data):
        self._attr_native_value = data.get("countdown_state")


class AutoPoweroffSensor(PandaPWRSensor):
    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Auto Poweroff", "auto_poweroff")

    def process_data(self, data):
        self._attr_native_value = data.get("auto_poweroff")


class CountdownSensor(PandaPWRSensor):
    def __init__(self, api, entry, device_id):
        super().__init__(api, entry, device_id, "Countdown", "countdown", "s")

    def process_data(self, data):
        self._attr_native_value = data.get("countdown")


class VoltageSensor(PandaPWRSensor):
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
        self._attr_native_value = data.get("voltage") or 0.0


class CurrentSensor(PandaPWRSensor):
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
        self._attr_native_value = data.get("current") or 0.0


class PowerSensor(PandaPWRSensor):
    def __init__(self, api, entry, device_id):
        super().__init__(
            api, entry, device_id, "Power", "power", UnitOfPower.WATT, "power"
        )

    def process_data(self, data):
        self._attr_native_value = data.get("power") or 0.0


class EnergyUsageSensor(PandaPWRSensor):
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
        self._attr_native_value = data.get("ele") or 0.0
