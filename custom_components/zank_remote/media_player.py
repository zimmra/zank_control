import json
import logging
import socket
import os
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
from homeassistant.const import (
    CONF_NAME,
    CONF_IP_ADDRESS,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PLAYING,
    STATE_UNKNOWN,
)

_LOGGER = logging.getLogger(__name__)

with open(os.path.join(os.path.dirname(__file__), "commands.json"), "r") as file:
    COMMANDS_DICT = json.load(file)

SUPPORTED_FEATURES = (
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

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the media player from a config entry."""
    async_add_entities([UDPMediaRemote(config_entry.data)])

class UDPMediaRemote(MediaPlayerEntity):
    def __init__(self, device_info):
        self._name = device_info[CONF_NAME]
        self._ip_address = device_info[CONF_IP_ADDRESS]
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORTED_FEATURES

    def _send_command(self, command):
        udp_command = COMMANDS_DICT.get(command)
        if not udp_command:
            _LOGGER.error("Invalid command: %s", command)
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(udp_command.encode(), (self._ip_address, 1028))
        sock.close()

    def turn_on(self):
        self._send_command("power_toggle")
        self._state = STATE_OFF

    def turn_off(self):
        self._send_command("power_toggle")
        self._state = STATE_OFF

    def media_play(self):
        self._send_command("media_play")
        self._state = STATE_PLAYING

    def media_pause(self):
        self._send_command("media_pause")
        self._state = STATE_PAUSED

    def media_stop(self):
        self._send_command("media_stop")
        self._state = STATE_OFF

    def media_previous_track(self):
        self._send_command("media_previous_track")

    def media_next_track(self):
        self._send_command("media_next_track")

    def volume_up(self):
        self._send_command("volume_up")

    def volume_down(self):
        self._send_command("volume_down")

    def mute_volume(self, mute):
        self._send_command("mute_volume")
