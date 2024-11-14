"""Binary sensor platform for PandaPWR integration in Home Assistant."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the binary sensor platform from a config entry."""
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [PowerStateBinarySensor(api, entry), UsbStateBinarySensor(api, entry)], True
    )


class PandaPWRBinarySensor(BinarySensorEntity):
    """Base class for a PandaPWR binary sensor."""

    def __init__(self, api, entry):
        """Initialize the binary sensor."""
        self._api = api
        self._entry = entry
        self._attr_is_on = None
        self._attr_available = False
        self._device_id = f"pandapwr_{self._entry.data['ip_address']}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            data = await self._api.get_data()
            self._attr_available = True
            self.process_data(data)
        except Exception:
            self._attr_available = False

    async def async_added_to_hass(self):
        """Subscribe to update signal."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass, f"{DOMAIN}_update_signal", self.async_update
            )
        )

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
        """Process data received from the API."""
        raise NotImplementedError


class PowerStateBinarySensor(PandaPWRBinarySensor):
    """Binary sensor for monitoring the power state of a PandaPWR device."""

    def __init__(self, api, entry):
        super().__init__(api, entry)
        self._attr_name = "Power State"
        self._attr_device_class = "power"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"{self._device_id}_power_state"

    def process_data(self, data):
        """Process power state data from the API."""
        self._attr_is_on = data.get("power_state") == 1


class UsbStateBinarySensor(PandaPWRBinarySensor):
    """Binary sensor for monitoring the USB state of a PandaPWR device."""

    def __init__(self, api, entry):
        super().__init__(api, entry)
        self._attr_name = "USB State"
        self._attr_device_class = "power"  # Set to "power" for on/off display
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_unique_id = f"{self._device_id}_usb_state"

    def process_data(self, data):
        """Process USB state data from the API."""
        self._attr_is_on = (
            data.get("usb_state") == 1
        )  # Display as "on" when 1, "off" when 0
