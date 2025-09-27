from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, DEVICE_ID,SENSOR_TYPES
from .websocket_client import WebSocketClient
from homeassistant.config_entries import ConfigEntry

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    entry_id = entry.entry_id
    data = hass.data[DOMAIN][entry_id]
    if DOMAIN in hass.data and "ws_client" not in hass.data[DOMAIN]:
        hass.data[DOMAIN]["ws_client"] = WebSocketClient(hass)
        _LOGGER.debug(f"{DOMAIN} websocket url: {hass.data[DOMAIN][entry.entry_id]["wsurl"]}")
        await hass.data[DOMAIN]["ws_client"].connect(hass.data[DOMAIN][entry.entry_id]["wsurl"])
    else:
        _LOGGER.warning("WebSocket client not found in hass.data")

    entities = []
    for key, (name, unit) in SENSOR_TYPES.items():
        entities.append(MultiSensor(key, hass.data[DOMAIN]["ws_client"],name, unit))
    async_add_entities(entities)

class MultiSensor(SensorEntity):
    def __init__(self,  key, websocketclient,name, unit):
        self._websocketclient= websocketclient
        self._key = key
        self._unique_id="recmbs_"+key
        self._attr_name = f"{DOMAIN} {name}"
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = "measurement"
        self._state = None
        _LOGGER.info("creating REC BMS entity key:"+key+" name:"+self._attr_name+" unit:"+unit+" nuique_id:"+self._unique_id)

    @property
    def state(self):
        old_value=self._state
        new_value=self._websocketclient.data.get(self._key)
        self._state=new_value
        if self._state is not None:   
            self.native_value=new_value
            self._attr_native_value = new_value
            #self.async_write_ha_state()
            self._attr_available = True
            #_LOGGER.debug("Updated "+str(self.name)+" to "+str(new_value) +" was "+ str(old_value))
            return new_value
        else:
            _LOGGER.debug(f"{self.name} has no state yet.")
            return None
