"""The REC BMS integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN,DEVICE_ID
from .websocket_client import WebSocketClient

import logging

PLATFORMS: Final = ["sensor","binary_sensor"]
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    hass.data[DOMAIN].setdefault("entities", [])
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("recbms websocket url:"+entry.data["wsurl"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    hass.data[DOMAIN].pop("ws_client")
    return True

