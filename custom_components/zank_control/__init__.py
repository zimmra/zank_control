import logging
from homeassistant import config_entries
from homeassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from homeassistant.components.remote import DOMAIN as REMOTE_DOMAIN
from homeassistant.const import CONF_IP_ADDRESS, CONF_NAME

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    if DOMAIN not in config:
        return True

    for entry in config[DOMAIN]:
        name = entry[CONF_NAME]
        ip_address = entry[CONF_IP_ADDRESS]

        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={"source": config_entries.SOURCE_IMPORT},
                data={
                    CONF_NAME: name,
                    CONF_IP_ADDRESS: ip_address,
                    MEDIA_PLAYER_DOMAIN: True,
                    REMOTE_DOMAIN: True,
                },
            )
        )

    return True
