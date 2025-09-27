from aiohttp import ClientSession, WSMsgType, ClientConnectorError, ClientTimeout
from websockets.exceptions import ConnectionClosedError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from datetime import datetime

import asyncio
import json
import logging
import websockets

_LOGGER = logging.getLogger(__name__)

class WebSocketClient:
    def __init__(self, hass):
        self.hass = hass
        self.data = {}

    async def connect(self,wsurl):
        self.wsurl = wsurl
        async def listen():
            _LOGGER.debug("connecting to websocker"+self.wsurl )
            try:            
                async with websockets.connect(self.wsurl) as websocket:
                    while True:
                            data = await websocket.recv()
                            #_LOGGER.debug("websocket received data"+str(data)[:50])
                            recbms_json = parse_bms_message(data)
                            if recbms_json:
                                    self.data.update(recbms_json)
                                    update_state(self.hass, recbms_json)
                                    self.hass.bus.async_fire("recbms_event", recbms_json)                                        
            except ConnectionClosedError as e:
                _LOGGER.warning("RECBMS WebSocket connection closed: %s", e)
                await asyncio.sleep(5)  # Wait before reconnecting
            except asyncio.CancelledError:
                _LOGGER.info("RECBMS WebSocket listener cancelled.")
                raise
            except Exception as e:
                _LOGGER.error("RECBMS Unexpected error: %s", e)
                await asyncio.sleep(10)
        asyncio.create_task(listen())
        self.hass.bus.async_listen_once("homeassistant_stop", lambda event: ws.close())

def parse_bms_message(raw):
    try:
        recbms_json=json.loads(raw)
        if "type" in recbms_json and recbms_json.get("type") == "status":
            recbms_json=recbms_json["bms_array"]["master"]
            recbms_json["last_update"]=datetime.now()
            # recbms_json["charging"]=
            # recbms_json["Discharging"]=
            return recbms_json
        else:
            return {}
    except json.JSONDecodeError:
        return None

def update_state(hass, data):
    if not data:
        return

    time_remaining = data["time_remaining"]
    if isinstance(time_remaining, str):
        time_remaining = time_remaining.replace("<br>", "")
    mincell = data["mincell"]
    maxcell = data["maxcell"]
    ibat = data["ibat"]
    tmax = data["tmax"]
    vbat = data["vbat"]
    soc = data["soc"]
    soh = data["soh"]

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
    hass.states.async_set(
        "sensor.recbms_last_update",
        soh,
        {"unit_of_measurement": "timestamp", "friendly_name": "Last update"},
    )    

