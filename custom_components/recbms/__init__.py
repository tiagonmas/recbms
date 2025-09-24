"""The REC BMS integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN

from .websocket_client import WebSocketClient

# _PLATFORMS: list[Platform] = [Platform.SENSOR]


# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
# type RECBMS_WSURLConfigEntry = ConfigEntry[RECBMSWSURL]


# # TODO Update entry annotation
# async def async_setup_entry(hass: HomeAssistant, entry: RECBMS_WSURLConfigEntry) -> str:
#     """Set up REC BMS from a config entry."""

#     # TODO 1. Create API instance
#     # TODO 2. Validate the API connection (and authentication)
#     # TODO 3. Store an API object for your platforms to access
#     # entry.runtime_data = MyAPI(...)

#     await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

#     return True


# TODO Update entry annotation
# async def async_unload_entry(
#     hass: HomeAssistant, entry: RECBMS_WSURLConfigEntry
# ) -> str:
#     """Unload a config entry."""
#     return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)


async def async_setup(hass, config: dict):
    ws_client = WebSocketClient(hass)
    await ws_client.connect()
    hass.data.setdefault(DOMAIN, {})
    hass.data["recbms"] = ws_client
    return True
