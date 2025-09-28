from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([MyBinarySensor()])

class MyBinarySensor(BinarySensorEntity):
    def __init__(self):
        self._is_on = False
        self._attr_name = "My Custom Binary Sensor"

    @property
    def is_on(self):
        return self._is_on
