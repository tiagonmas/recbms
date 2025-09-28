"""Constants for the REC BMS integration."""

DOMAIN = "recbms"
DEVICE_ID = "recbms_202509"
CONF_WSURL="ws://192.168.8.3/ws"
CONF_NAME="RECBMS"

SENSOR_TYPES = {
    "time_remaining": ["MultiSensor","Time remaining", "","mdi:clock-time-eight"],
    "time_remaining_mins": ["MultiSensor","Minutes remaining", "min","mdi:clock-time-eight"],
    "time_remaining_hours": ["MultiSensor","Hours remaining", "H","mdi:clock-time-eight"],
    "mincell": ["MultiSensor","Minimum cell voltage", "V","mdi:battery"],
    "maxcell": ["MultiSensor","Maximum cell voltage", "V","mdi:battery"],
    "mincell": ["MultiSensor","Minimum cell voltage", "V","mdi:battery"],
    "ibat": ["MultiSensor","Current", "A","mdi:flash-triangle-outline"],
    "tmax": ["MultiSensor","Max Temperature", "°C","mdi:hydraulic-oil-temperature"],
    "vbat": ["MultiSensor","Pack Voltage", "V","mdi:battery"],
    "soc": ["MultiSensor","State of Charge", "%","mdi:percent"],
    "soc100": ["MultiSensor","State of Charge100", "%","mdi:percent"],
    "soh": ["MultiSensor","State of Health", "%","mdi:medication"],
    "last_update": ["MultiSensor","Last Update", "","mdi:clock-time-eight"],
    "charging": ["MultiSensor","Charging", "A","mdi:battery"],
    "discharging": ["MultiSensor","Discharging", "A","mdi:battery"]
}
