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
import re

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
                            recbms_json = parse_bms_message(data)
                            if recbms_json:
                                    # _LOGGER.debug("status:"+str(recbms_json))
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
                _LOGGER.error("RECBMS Unexpected websocket error: %s", e)
                await asyncio.sleep(10)
        asyncio.create_task(listen())
        self.hass.bus.async_listen_once("homeassistant_stop", lambda event: self.hass.data[DOMAIN]["ws_client"].close())

def parse_bms_message(raw):
    try:
        recbms_json=json.loads(raw)
        if "type" in recbms_json and recbms_json.get("type") == "status":
            #_LOGGER.debug("status: "+str(recbms_json))
            recbms_json=recbms_json["bms_array"]["master"]
            recbms_json["last_update"]=datetime.now().replace(microsecond=0)
            recbms_json["time_remaining"] = recbms_json["time_remaining"].replace("<br>", "")
            hours, minutes = extract_time(recbms_json["time_remaining"])
            if hours is not None and minutes is not None:
                recbms_json["time_remaining_mins"]=minutes+hours*60
                recbms_json["time_remaining_hours"]= round(hours + (minutes / 60),1)
            recbms_json["soh"]=round(recbms_json["soh"],4)
            recbms_json["soc"]=round(recbms_json["soc"],4)
            recbms_json["soc100"]=round(recbms_json["soc"]*100,2)
            # recbms_json["charging"]=
            # recbms_json["Discharging"]=
            return recbms_json
        else:
            return {}
    except json.JSONDecodeError:
        _LOGGER.error("RECBMS JSONDecodeError: %s", e)
    except Exception as e:
        _LOGGER.error("RECBMS parse_bms_message error: %s", e)
        _LOGGER.error("RECBMS parse_bms_message error2:"+str(recbms_json))
        return None

def extract_time(text):
    # Match patterns like "8 h" and "49 min"
    try:
        match = re.search(r'(\d+)\s*h\s*(\d+)\s*min', text)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            return hours, minutes
        else:
            return None, None
    except Exception as e:
        _LOGGER.error("RECBMS extract_time: %s", e)
        _LOGGER.error("RECBMS extract_time2: "+text)
        return None, None

def update_state(hass, data):
    if not data:
        return

    time_remaining = data["time_remaining"]
    mincell = data["mincell"]
    maxcell = data["maxcell"]
    ibat = data["ibat"]
    tmax = data["tmax"]
    vbat = data["vbat"]
    soc = data["soc"]
    soh = data["soh"]

    hass.states.async_set(
        "sensor.recbms_state_time_remaining",
        time_remaining,
        {"unit_of_measurement": "H", "friendly_name": "Time remaining"},
    )
    hass.states.async_set(
        "sensor.recbms_state_mincell",
        mincell,
        {"unit_of_measurement": "V", "friendly_name": "Minimum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_state_maxcell",
        maxcell,
        {"unit_of_measurement": "V", "friendly_name": "Maximum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_state_mincell",
        mincell,
        {"unit_of_measurement": "V", "friendly_name": "Minimum cell voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_state_ibat",
        ibat,
        {"unit_of_measurement": "A", "friendly_name": "Current"},
    )
    hass.states.async_set(
        "sensor.recbms_state_tmax",
        tmax,
        {"unit_of_measurement": "°C", "friendly_name": "Max temperature"},
    )
    hass.states.async_set(
        "sensor.recbms_state_vbat",
        vbat,
        {"unit_of_measurement": "V", "friendly_name": "Voltage"},
    )
    hass.states.async_set(
        "sensor.recbms_state_soc",
        soc,
        {"unit_of_measurement": "%", "friendly_name": "State of charge"},
    )
    hass.states.async_set(
        "sensor.recbms_state_soh",
        soh,
        {"unit_of_measurement": "%", "friendly_name": "State of Health"},
    )
    hass.states.async_set(
        "sensor.recbms_state_last_update",
        datetime.now().replace(microsecond=0),
        {"unit_of_measurement": "", "friendly_name": "Last update"},
    )    

