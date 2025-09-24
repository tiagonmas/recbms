import asyncio
import json
import logging

import websockets

_LOGGER = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(self, hass):
        self.hass = hass
        self.url = "ws://192.168.8.2/ws"  # Replace with your device's IP and port

    async def connect(self):
        async def listen():
            _LOGGER.info("Connecting to websocket.")
            async with websockets.connect(self.url) as websocket:
                while True:
                    _LOGGER.debug("received data")
                    data = await websocket.recv()
                    data_json = parse_bms_message(data)
                    if "type" in data_json:
                        if data_json.get("type") == "status":
                            update_state(self.hass, data_json)
                            # self.hass.bus.async_fire("recbms_event", {"data": data})

        asyncio.create_task(listen())


def parse_bms_message(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def update_state(hass, data):
    if not data:
        return

    time_remaining = data["bms_array"]["master"]["time_remaining"]
    if isinstance(time_remaining, str):
        time_remaining = time_remaining.replace("<br>", "")
    mincell = data["bms_array"]["master"]["mincell"]
    maxcell = data["bms_array"]["master"]["maxcell"]
    ibat = data["bms_array"]["master"]["ibat"]
    tmax = data["bms_array"]["master"]["tmax"]
    vbat = data["bms_array"]["master"]["vbat"]
    soc = data["bms_array"]["master"]["soc"]
    soh = data["bms_array"]["master"]["soh"]

    hass.states.async_set(
        "sensor.recbms_time_remaining",
        time_remaining,
        {"unit_of_measurement": "H", "friendly_name": "Time remaining"},
    )
    hass.states.async_set(
        "sensor.recbms_mincell",
        mincell,
        {"unit_of_measurement": "V", "friendly_name": "Minimum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_maxcell",
        maxcell,
        {"unit_of_measurement": "V", "friendly_name": "Maximum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_mincell",
        mincell,
        {"unit_of_measurement": "V", "friendly_name": "Minimum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_ibat",
        ibat,
        {"unit_of_measurement": "A", "friendly_name": "Current"},
    )
    hass.states.async_set(
        "sensor.recbms_tmax",
        tmax,
        {"unit_of_measurement": "°C", "friendly_name": "Max temperature"},
    )
    hass.states.async_set(
        "sensor.recbms_vbat",
        vbat,
        {"unit_of_measurement": "V", "friendly_name": "Voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_soc",
        soc,
        {"unit_of_measurement": "%", "friendly_name": "State of charge"},
    )
    hass.states.async_set(
        "sensor.recbms_soh",
        soh,
        {"unit_of_measurement": "%", "friendly_name": "State of Health"},
    )
