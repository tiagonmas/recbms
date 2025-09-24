from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN, DEVICE_ID


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensor = WebSocketSensor()
    async_add_entities([sensor])

    async def handle_event(event):
        sensor.update_state(event.data["data"])
        sensor.async_write_ha_state()

    hass.bus.async_listen("recbms_event", handle_event)


class WebSocketSensor(Entity):
    def __init__(self):
        self._state = None
        self._name = "WebSocket Sensor"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update_state(self, data):
        self._state = data
