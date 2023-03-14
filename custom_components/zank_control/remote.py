import asyncio
import json
import socket
from homeassistant.components.remote import (
    ATTR_NUM_REPEATS,
    ATTR_DELAY_SECS,
    RemoteEntity,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect

DOMAIN = "zank_control"

# Load CMD_MAPPING from the JSON file
with open("cmd_mapping.json", "r") as f:
    CMD_MAPPING = json.load(f)

UDP_PORT = 1028

def setup_platform(hass, config, add_entities, discovery_info=None):
    if DOMAIN not in hass.data or "remote" not in hass.data[DOMAIN]:
        return

    entities = []
    for conf in hass.data[DOMAIN]["remote"]:
        name = conf.get("name")
        udp_ip = conf.get("udp_ip")
        entity_id = conf.get("entity_id")

        entities.append(UDPRemote(name, udp_ip, entity_id))

    add_entities(entities)

class UDPRemote(RemoteEntity):
    def __init__(self, name, udp_ip, entity_id):
        self._name = name
        self._udp_ip = udp_ip
        self._entity_id = entity_id

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._entity_id

    def send_udp_command(self, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(command.encode(), (self._udp_ip, UDP_PORT))

    async def async_send_command(self, command, **kwargs):
        num_repeats = kwargs.get(ATTR_NUM_REPEATS, 1)
        delay_secs = kwargs.get(ATTR_DELAY_SECS, 0.5)

        for _ in range(num_repeats):
            for single_command in command:
                if single_command in CMD_MAPPING:
                    self.send_udp_command(CMD_MAPPING[single_command])
                else:
                    self.send_udp_command(single_command)

                await asyncio.sleep(delay_secs)
