"""Switch platform for PandaPWR integration in Home Assistant."""

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up switch platform for PandaPWR."""
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [PowerSwitch(api, entry, hass), UsbSwitch(api, entry, hass)], True
    )


class PandaPWRSwitch(SwitchEntity):
    """Base class for a PandaPWR switch."""

    def __init__(self, api, entry, hass):
        """Initialize the switch."""
        self._api = api
        self._entry = entry
        self._hass = hass
        self._attr_is_on = None
        self._device_id = f"pandapwr_{self._entry.data['ip_address']}"

    async def async_update(self):
        """Fetch latest state data from the device."""
        data = await self._api.get_data()
        self.process_data(data)

    @property
    def device_info(self):
        """Return device information for grouping in the UI."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "Panda PWR",
            "manufacturer": "Panda",
            "model": "PWR Device",
            "sw_version": "1.0",
        }

    def process_data(self, data):
        """Process API data."""
        raise NotImplementedError


class PowerSwitch(PandaPWRSwitch):
    """Switch entity for controlling the power state of a PandaPWR device."""

    def __init__(self, api, entry, hass):
        super().__init__(api, entry, hass)
        self._attr_name = "Power Switch"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_unique_id = f"{self._device_id}_power_switch"

    async def async_turn_on(self):
        """Turn on the power switch."""
        await self._api.set_power_state(1)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn off the power switch."""
        await self._api.set_power_state(0)
        self._attr_is_on = False
        self.async_write_ha_state()

    def process_data(self, data):
        """Process power state data from the API."""
        self._attr_is_on = data.get("power_state") == 1


class UsbSwitch(PandaPWRSwitch):
    """Switch entity for controlling the USB state of a PandaPWR device."""

    def __init__(self, api, entry, hass):
        super().__init__(api, entry, hass)
        self._attr_name = "USB Switch"
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_unique_id = f"{self._device_id}_usb_switch"

    async def async_turn_on(self):
        """Turn on the USB switch."""
        await self._api.set_usb_state(1)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn off the USB switch."""
        await self._api.set_usb_state(0)
        self._attr_is_on = False
        self.async_write_ha_state()

    def process_data(self, data):
        """Process USB state data from the API."""
        self._attr_is_on = data.get("usb_state") == 1
