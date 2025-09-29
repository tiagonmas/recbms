from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, DEVICE_ID,SENSOR_TYPES

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    entities = []
    for key, (sensortype,name, unit,device_class,state_class,icon) in SENSOR_TYPES.items():
        if sensortype == "MyBinarySensor":
            entities.append(MyBinarySensor(key, hass.data[DOMAIN]["ws_client"],name, unit,device_class,state_class,icon))
    async_add_entities(entities)
    _LOGGER.debug(f"Sensor Entities size: {len(hass.data[DOMAIN]["entities"])}")
    hass.data[DOMAIN]["entities"].extend(entities)
    _LOGGER.debug(f"Sensor Entities new size: {len(hass.data[DOMAIN]["entities"])}")    

class MyBinarySensor(BinarySensorEntity):
    def __init__(self,  key, websocketclient,name, unit,device_class,state_class,icon):
        self._websocketclient= websocketclient
        self._is_on = False
        self._key = key
        self._unique_id="recmbs_"+key
        self._attr_unique_id="recmbs_"+key
        self._attr_name = f"{DOMAIN} {name}"
        self._attr_icon=icon
        _LOGGER.info("creating REC BMS MyBinarySensor key:"+key+" name:"+self._attr_name+" unit:"+str(unit)+" unique_id:"+self._unique_id)

    @property
    def is_on(self):
        return self._is_on


    def update_value(self, new_state: bool):
        if self._is_on != new_state:
            _LOGGER.debug("Binary Sensor Updated "+str(self._attr_unique_id)+" to "+str(new_state) +" was "+ str(self._is_on))
            self._is_on = new_state
            _LOGGER.debug("Binary Sensor Updated:"+ str(self._is_on))
            self.async_write_ha_state()
