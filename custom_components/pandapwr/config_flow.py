import voluptuous as vol
from homeassistant import config_entries

from .api import PandaPWRApi
from .const import DOMAIN


class PandaPWRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input:
            ip_address = user_input["ip_address"]
            api = PandaPWRApi(ip_address)
            if await api.test_connection():
                return self.async_create_entry(title="Panda PWR", data=user_input)
            errors["base"] = "cannot_connect"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("ip_address"): str}),
            errors=errors,
        )
