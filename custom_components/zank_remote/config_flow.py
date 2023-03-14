import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from . import DOMAIN

class UDPFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input["ip_address"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ip_address"): str,
                    vol.Required("name"): str,
                }
            ),
            errors=errors,
        )
