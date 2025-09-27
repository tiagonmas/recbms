"""Constants for the REC BMS integration."""

DOMAIN = "recbms"
DEVICE_ID = "recbms_202509"
CONF_WSURL="ws://192.168.8.3/ws"
CONF_NAME="RECBMS"

SENSOR_TYPES = {
    "time_remaining": ["Time remaining", "","mdi:clock-time-eight"],
    "time_remaining_mins": ["Minutes remaining", "min","mdi:clock-time-eight"],
    "time_remaining_hours": ["Hours remaining", "H","mdi:clock-time-eight"],
    "mincell": ["Minimum cell voltage", "V","mdi:battery"],
    "maxcell": ["Maximum cell voltage", "V","mdi:battery"],
    "mincell": ["Minimum cell voltage", "V","mdi:battery"],
    "ibat": ["Current", "A","mdi:flash-triangle-outline"],
    "tmax": ["Max Temperature", "°C","mdi:hydraulic-oil-temperature"],
    "vbat": ["Pack Voltage", "V","mdi:battery"],
    "soc": ["State of Charge", "%","mdi:percent"],
    "soh": ["State of Health", "%","mdi:medication"],
    "last_update": ["Last Update", "","mdi:clock-time-eight"],
    "charging": ["Charging", "A","mdi:battery"],
    "discharging": ["Discharging", "A","mdi:battery"]
}
