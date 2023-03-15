import json
import logging
import socket
import time
import os
from homeassistant.components.remote import (
    RemoteEntity,
    ATTR_NUM_REPEATS,
    ATTR_DELAY_SECS,
)
from homeassistant.const import CONF_NAME, CONF_IP_ADDRESS

_LOGGER = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "commands.json"), "r") as file:
    COMMANDS_DICT = json.load(file)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the remote from a config entry."""
    async_add_entities([UDPRemote(config_entry.data)])

class UDPRemote(RemoteEntity):
    def __init__(self, device_info):
        self._name = device_info[CONF_NAME]
        self._ip_address = device_info[CONF_IP_ADDRESS]

    @property
    def name(self):
        return self._name

    def _send_command(self, command, num_repeats=1, delay_secs=0.0):
        udp_command = COMMANDS_DICT.get(command)
        if not udp_command:
            _LOGGER.error("Invalid command: %s", command)
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(num_repeats):
            sock.sendto(udp_command.encode(), (self._ip_address, 1028))
            time.sleep(delay_secs)
        sock.close()

    def send_command(self, command, **kwargs):
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, 1)
        delay_secs = kwargs.get(ATTR_DELAY_SECS, 0.0)
        self._send_command(command, num_repeats, delay_secs)
