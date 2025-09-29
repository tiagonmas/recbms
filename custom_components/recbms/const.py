"""Constants for the REC BMS integration."""

DOMAIN = "recbms"
DEVICE_ID = "recbms_202509"
CONF_WSURL="ws://192.168.8.3/ws"
CONF_NAME="RECBMS"

SENSOR_TYPES = {
    #key: sensortype,name, unit,device_class,state_class,icon
    "time_remaining": ["MultiSensor","Time remaining", None,None,None,"mdi:clock-time-eight"],
    "time_remaining_mins": ["MultiSensor","Minutes remaining", "min","duration","measurement","mdi:clock-time-eight"],
    "time_remaining_hours": ["MultiSensor","Hours remaining", "h","duration","measurement","mdi:clock-time-eight"],
    "mincell": ["MultiSensor","Minimum cell voltage", "V","voltage","measurement","mdi:battery"],
    "maxcell": ["MultiSensor","Maximum cell voltage", "V","voltage","measurement","mdi:battery"],
    "mincell": ["MultiSensor","Minimum cell voltage", "V","voltage","measurement","mdi:battery"],
    "ibat": ["MultiSensor","Current", "A","current","measurement","mdi:flash-triangle-outline"],
    "tmax": ["MultiSensor","Max Temperature", "°C","temperature","measurement","mdi:hydraulic-oil-temperature"],
    "vbat": ["MultiSensor","Pack Voltage", "V","voltage","measurement","mdi:battery"],
    "soc": ["MultiSensor","State of Charge", "%","battery","measurement","mdi:percent"],
    "soc100": ["MultiSensor","State of Charge100", "%","battery","measurement","mdi:percent"],
    "soh": ["MultiSensor","State of Health", "%","battery","measurement","mdi:medication"],
    "last_update": ["MultiSensor","Last Update", None,None,None,"mdi:clock-time-eight"],
    "charging": ["MyBinarySensor","Charging", None,None,None,"mdi:battery"],
    "discharging": ["MyBinarySensor","Discharging",None, None,None,"mdi:battery"]
}
