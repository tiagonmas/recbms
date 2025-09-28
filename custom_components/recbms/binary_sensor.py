from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, DEVICE_ID,SENSOR_TYPES

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    #async_add_entities([MyBinarySensor(key, websocketclient, name, unit, icon)])
    entities = []
    for key, (sensortype,name, unit,icon) in SENSOR_TYPES.items():
        if sensortype == "MyBinarySensor":
            entities.append(MyBinarySensor(key, hass.data[DOMAIN]["ws_client"],name, unit,icon))
    async_add_entities(entities)
    return  

class MyBinarySensor(BinarySensorEntity):
    def __init__(self,  key, websocketclient,name, unit,icon):
        self._websocketclient= websocketclient
        self._is_on = False
        self._key = key
        self._unique_id="recmbs_"+key
        self._attr_unique_id="recmbs_"+key
        self._attr_name = f"{DOMAIN} {name}"
        self._attr_icon=icon
        _LOGGER.info("creating REC BMS MyBinarySensor key:"+key+" name:"+self._attr_name+" unit:"+unit+" unique_id:"+self._unique_id)

    @property
    def is_on(self):
        return self._is_on

    @property
    def state(self):
        #_LOGGER.debug(f"Binary Update for {self._attr_name} now:{str(self._attr_is_on)}")
        old_value=self._attr_is_on
        json_value=self._websocketclient.data.get(self._key)
        #_LOGGER.debug(f"Binary Update for {self._attr_name} json:{str(json_value)}")
        if json_value == True:
            self._attr_is_on=True
        else:
            self._attr_is_on=False
        return self._attr_is_on