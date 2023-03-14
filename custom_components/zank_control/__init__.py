from homeassistant.helpers import config_entry_flow
from homeassistant import config_entries

from .const import DOMAIN

async def async_setup(hass, config):
    return True

async def _async_has_devices(hass, domain):
    return True
