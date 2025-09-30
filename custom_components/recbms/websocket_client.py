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
        self.token = "YOUR_LONG_LIVED_ACCESS_TOKEN"
        self.ping_interval = 30
        self.ping_timeout = 10
        self.max_reconnect_delay = 300  # 5 minutes


    async def run(self,wsurl):
        self.uri=wsurl
        reconnect_delay = 5
        while True:
            try:
                async with websockets.connect(
                    self.uri,
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout
                ) as ws:
                    _LOGGER.info("RECBMS Connected to WebSocket API")
                    reconnect_delay = 5  # reset delay on success
                    #await self.authenticate(ws)
                    await self.listen(ws)
            except Exception as e:
                _LOGGER.warning(f"RECBMS WebSocket error: {e}")
                _LOGGER.info(f"RECBMS Reconnecting in {reconnect_delay} seconds...")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, self.max_reconnect_delay)

    async def authenticate(self, ws):
        await ws.send(json.dumps({"type": "auth", "access_token": self.token}))
        response = await ws.recv()
        data = json.loads(response)
        if data.get("type") != "auth_ok":
            raise Exception("RECBMS Authentication failed")
        _LOGGER.info("RECBMS Authenticated successfully")

    async def listen(self, ws):
        try:
            while True:
                data = await ws.recv()
                recbms_json = parse_bms_message(data)
                if recbms_json:
                        #self.hass.bus.async_fire("recbms_event", recbms_json)
                        update_entities(self.hass.data[DOMAIN]["entities"],recbms_json)                
                #_LOGGER.debug(f"RECBMS Received: {data}")
        except websockets.exceptions.ConnectionClosedError as e:
            _LOGGER.warning(f"RECBMS Connection closed: {e}")
        finally:
            await ws.close(code=1000, reason="Normal closure")

def update_entities(entities,recbms_json):
    for entity in entities:
        #_LOGGER.info(f"will update {entity._key}")
        entity.update_value(recbms_json.get(entity._key))
        

def parse_bms_message(raw):
    try:
        recbms_json=json.loads(raw)
        if "type" in recbms_json and recbms_json.get("type") == "status":
            recbms_json=recbms_json["bms_array"]["master"]
            recbms_json["last_update"]=datetime.now().replace(microsecond=0)
            recbms_json["time_remaining"] = recbms_json["time_remaining"].replace("<br>", "")
            hours, minutes = extract_time(recbms_json["time_remaining"])
            if hours is not None and minutes is not None:
                recbms_json["time_remaining_mins"]=minutes+hours*60
                recbms_json["time_remaining_hours"]= round(hours + (minutes / 60),1)
            recbms_json["soh"]=round(recbms_json["soh"]*100,4)
            recbms_json["soc"]=round(recbms_json["soc"],4)
            recbms_json["soc100"]=round(recbms_json["soc"]*100,2)
            if recbms_json["ibat"]>0:
                #_LOGGER.debug("RECBMS charging:"+str( recbms_json["ibat"]))
                recbms_json["charging"]=True
                recbms_json["discharging"]=False
            else:
                #_LOGGER.debug("RECBMS discharging"+str( recbms_json["ibat"]))
                recbms_json["charging"]=False
                recbms_json["discharging"]=True
            return recbms_json
        else:
            return {}
    except json.JSONDecodeError:
        _LOGGER.error("RECBMS JSONDecodeError: %s", e)
    except Exception as e:
        _LOGGER.error("RECBMS parse_bms_message error: %s", e)
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
        return None, None
