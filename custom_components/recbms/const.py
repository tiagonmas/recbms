"""Constants for the REC BMS integration."""

DOMAIN = "recbms"
DEVICE_ID = "recbms_202509"
CONF_WSURL="ws://192.168.8.3/ws"
CONF_NAME="RECBMS"

SENSOR_TYPES = {
    "time_remaining": ["Time remaining", "H"],
    "mincell": ["Minimum cell voltage", "V",],
    "maxcell": ["Maximum cell voltage", "V"],
    "mincell": ["Minimum cell voltage", "V"],
    "ibat": ["Current", "A"],
    "tmax": ["Max Temperature", "°C"],
    "vbat": ["Pack Voltage", "V"],
    "soc": ["State of Charge", "%"],
    "soh": ["State of Health", "%"],
    "last_update": ["Last Update", "timestamp"],
    "charging": ["Charging", "A"],
    "discharging": ["Discharging", "A"]
}
