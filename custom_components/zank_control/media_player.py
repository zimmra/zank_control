import asyncio
import json
import socket

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_TURN_ON,
    SUPPORT_TURN_OFF,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_NEXT_TRACK,
    SUPPORT_STOP,
    SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_STEP,
)
from homeassistant.components.remote import RemoteEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

DOMAIN = "zank_control"
CONF_NAME = "name"

# Load CMD_MAPPING from the JSON file
with open("cmd_mapping.json", "r") as f:
    CMD_MAPPING = json.load(f)

UDP_PORT = 1028

def setup_platform(hass, config, add_entities, discovery_info=None):
    if DOMAIN not in hass.data or "media_player" not in hass.data[DOMAIN]:
        return

    entities = []
    for conf in hass.data[DOMAIN]["media_player"]:
        name = conf.get(CONF_NAME)
        udp_ip = conf.get("udp_ip")
        entity_id = conf.get("entity_id")

        media_player = UDPMediaPlayer(name, udp_ip, entity_id)
        remote = UDPRemote(f"{name} Remote", udp_ip, f"remote.{entity_id}_remote")
        entities.extend([media_player, remote])

    add_entities(entities)

class UDPMediaPlayer(MediaPlayerEntity):
    def __init__(self, name, udp_ip, entity_id):
        self._name = name
        self._udp_ip = udp_ip
        self._entity_id = entity_id
        self._state = None
        self._volume_muted = False

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._entity_id

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return (
            SUPPORT_PAUSE
            | SUPPORT_PLAY
            | SUPPORT_TURN_ON
            | SUPPORT_TURN_OFF
            | SUPPORT_PREVIOUS_TRACK
            | SUPPORT_NEXT_TRACK
            | SUPPORT_STOP
            | SUPPORT_VOLUME_MUTE
            | SUPPORT_VOLUME_STEP
        )

    @property
    def is_volume_muted(self):
        return self._volume_muted

    def send_udp_command(self, command):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(command.encode(), (self._udp_ip, UDP_PORT))

    def turn_on(self):
        self.send_udp_command(CMD_MAPPING["power_toggle"])
        self._state = "on"

    def turn_off(self):
        self.send_udp_command(CMD_MAPPING["power_toggle"])
        self._state = "off"

    def media_play(self):
        self.send_udp_command(CMD_MAPPING["media_play"])
        self._state = "playing"

    def media_pause(self):
        self.send_udp_command(CMD_MAPPING["media_pause"])
        self._state = "paused"

    def media_previous_track(self):
        self.send_udp_command(CMD_MAPPING["media_previous_track"])

    def media_next_track(self):
        self.send_udp_command(CMD_MAPPING["media_next_track"])

    def media_stop(self):
        self.send_udp_command(CMD_MAPPING["media_stop"])
        self._state = "idle"

    def volume_up(self):
        self.send_udp_command(CMD_MAPPING["volume_up"])

    def volume_down(self):
        self.send_udp_command(CMD_MAPPING["volume_down"])

    def mute_volume(self, mute):
        self.send_udp_command(CMD_MAPPING["mute_volume"])
        self._volume_muted = mute

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
