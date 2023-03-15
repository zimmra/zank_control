"""The Zank Remote integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "zank_remote"
_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["remote", "media_player"]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Zank Remote component."""
    _LOGGER.debug("Setting up zank_remote integration")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Zank Remote from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
