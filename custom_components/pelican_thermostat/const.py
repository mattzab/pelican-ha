"""Constants for the Pelican Thermostat integration."""
from __future__ import annotations

DOMAIN = "pelican_thermostat"

# Configuration keys
CONF_BASE_URL = "base_url"
CONF_THERMOSTAT_NAME = "thermostat_name"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Default values
DEFAULT_BASE_URL = "https://demo.officeclimatecontrol.net/api.cgi"

# API parameters
API_USERNAME = "username"
API_PASSWORD = "password"
API_REQUEST = "request"
API_OBJECT = "object"
API_SELECTION = "selection"
API_VALUE = "value"

# API request types
REQUEST_GET = "get"
REQUEST_SET = "set"

# API objects
OBJECT_THERMOSTAT = "Thermostat"

# API values for get requests - Measurements
VALUE_TEMPERATURE = "temperature"
VALUE_HUMIDITY = "humidity"
VALUE_CO2_LEVEL = "co2Level"
VALUE_RUN_STATUS = "runStatus"
VALUE_SCHEDULE = "schedule"

# API values for get requests - Status
VALUE_STATUS = "status"  # Occupied/Vacant
VALUE_SET_BY = "setBy"  # Station/Remote/Schedule
VALUE_FRONT_KEYPAD = "frontKeypad"  # On/Off
VALUE_AUX_STATUS = "auxStatus"  # On/Off
VALUE_STATUS_DISPLAY = "statusDisplay"  # Human readable status

# API values for get requests - Fan
VALUE_FAN = "fan"  # Auto/On

# API values for get requests - Humidity settings
VALUE_HUMIDIFY_SETTING = "humidifySetting"
VALUE_DEHUMIDIFY_SETTING = "dehumidifySetting"
VALUE_HUMIDITY_CONTROL = "humidityControl"  # None/Humidify/Dehumidify/Full Control/Cool Only

# API values for get requests - CO2
VALUE_CO2_SETTING = "co2Setting"

# API values for get requests - System configuration
VALUE_HEAT_STAGES = "heatStages"
VALUE_COOL_STAGES = "coolStages"
VALUE_FAN_STAGES = "fanStages"
VALUE_SYSTEM_TYPE = "systemType"  # Conventional/HeatPump
VALUE_TEMPERATURE_FORMAT = "temperatureFormat"  # Fahrenheit/Celsius
VALUE_CYCLE_RATE = "cycleRate"
VALUE_ANTICIPATION_DEGREES = "anticipationDegrees"
VALUE_CALIBRATION_OFFSET = "calibrationOffset"

# API values for get requests - Temperature limits
VALUE_MIN_HEAT_SETTING = "minHeatSetting"
VALUE_MAX_HEAT_SETTING = "maxHeatSetting"
VALUE_MIN_COOL_SETTING = "minCoolSetting"
VALUE_MAX_COOL_SETTING = "maxCoolSetting"
VALUE_MIN_SAFE_TEMP = "minSafeTemp"
VALUE_MAX_SAFE_TEMP = "maxSafeTemp"

# API values for get requests - Device info
VALUE_SERIAL_NO = "serialNo"
VALUE_GATEWAY = "gateway"
VALUE_VERSION = "version"
VALUE_INSTALL_DATE = "installDate"

# API values for get requests - Notification settings
VALUE_NOTIFICATION_SENSITIVITY = "notificationSensitivity"
VALUE_NOTIFICATION_SETPOINT = "notificationSetpoint"
VALUE_NOTIFICATION_UNREACHABLE = "notificationUnreachable"

# API values for set requests
VALUE_SYSTEM = "system"
VALUE_HEAT_SETTING = "heatSetting"
VALUE_COOL_SETTING = "coolSetting"

# System modes
SYSTEM_AUTO = "Auto"
SYSTEM_HEAT = "Heat"
SYSTEM_COOL = "Cool"
SYSTEM_OFF = "Off"

# Fan modes
FAN_AUTO = "Auto"
FAN_ON = "On"

# Status values
STATUS_OCCUPIED = "Occupied"
STATUS_VACANT = "Vacant"

# Set by values
SET_BY_STATION = "Station"
SET_BY_REMOTE = "Remote"
SET_BY_SCHEDULE = "Schedule"

# Keypad values
KEYPAD_ON = "On"
KEYPAD_OFF = "Off"

# Schedule values
SCHEDULE_ON = "On"
SCHEDULE_OFF = "Off"

# Aux status values
AUX_ON = "On"
AUX_OFF = "Off"

# Configuration keys
CONF_POLL_INTERVAL = "poll_interval"

# Update interval
DEFAULT_POLL_INTERVAL = 70  # seconds (1 minute 10 seconds) 