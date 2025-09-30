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
        ws_client=WebSocketClient(hass)
        hass.data[DOMAIN]["ws_client"] = ws_client
        _LOGGER.debug(f"{DOMAIN} websocket url: {hass.data[DOMAIN][entry.entry_id]["wsurl"]}")
        hass.loop.create_task(ws_client.run(hass.data[DOMAIN][entry.entry_id]["wsurl"]))
    else:
        _LOGGER.warning("WebSocket client not found in hass.data")

    entities = []
    for key, (sensortype,name, unit,device_class,state_class,icon) in SENSOR_TYPES.items():
        if sensortype == "MultiSensor":
            entities.append(MultiSensor(key, hass.data[DOMAIN]["ws_client"],name, unit,device_class,state_class,icon))
    async_add_entities(entities)
    _LOGGER.debug(f"Sensor Entities size: {len(hass.data[DOMAIN]["entities"])}")
    hass.data[DOMAIN]["entities"].extend(entities)
    _LOGGER.debug(f"Sensor Entities new size: {len(hass.data[DOMAIN]["entities"])}")

class MultiSensor(SensorEntity):
    def __init__(self,  key, websocketclient,name, unit,device_class,state_class,icon):
        self._websocketclient= websocketclient
        self._key = key
        self._unique_id="recmbs_"+key
        self._attr_unique_id="recmbs_"+key
        self._attr_name = f"{DOMAIN} {name}"
        self._attr_icon=icon
        _LOGGER.debug(f"state_class {state_class} for {self._unique_id}")
        if state_class:
            self._attr_state_class = state_class
        if unit:
            self._attr_native_unit_of_measurement = unit
        if device_class:
            self._attr_device_class = device_class
        #_LOGGER.debug(f"state_class None for {self._unique_id}: {state_class} {self._attr_device_class} {self._attr_unit_of_measurement}")
        _LOGGER.info("creating REC BMS MultiSensor key:"+str(key)+" name:"+self._attr_name+" unit:"+str(unit)+" unique_id:"+self._unique_id)

    def update_value(self, value):
        if value != self._attr_native_value:
            self._attr_native_value = value
            self.async_write_ha_state()        


        
