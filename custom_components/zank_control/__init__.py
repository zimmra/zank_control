from homeassistant.helpers import config_entry_flow
from homeassistant import config_entries

from .const import DOMAIN

async def async_setup(hass, config):
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = config[DOMAIN]

    for entry in config[DOMAIN]:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": config_entries.SOURCE_IMPORT},
                data=entry,
            )
        )

    return True

async def _async_has_devices(hass, domain):
    return True
