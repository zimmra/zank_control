"""The zank_remote component."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "zank_remote"

PLATFORMS = ["media_player", "remote"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the zank_remote component from a config entry."""
    _LOGGER.debug("Setting up zank_remote integration")

    hass.data.setdefault(DOMAIN, {})

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
        """Handle removal of an entry."""
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
        if unload_ok:
            hass.data[DOMAIN].pop(entry.entry_id)
        return unload_ok

    return True