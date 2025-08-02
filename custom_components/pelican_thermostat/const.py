"""Constants for the Pelican Thermostat integration."""
from __future__ import annotations

DOMAIN = "pelican_thermostat"

# Configuration keys
CONF_BASE_URL = "base_url"
CONF_THERMOSTAT_NAME = "thermostat_name"

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

# API values for get requests
VALUE_TEMPERATURE = "temperature"
VALUE_HUMIDITY = "humidity"
VALUE_CO2_LEVEL = "co2Level"

# API values for set requests
VALUE_SYSTEM = "system"
VALUE_HEAT_SETTING = "heatSetting"
VALUE_COOL_SETTING = "coolSetting"
VALUE_HEAT_MIN = "heatMin"
VALUE_HEAT_MAX = "heatMax"
VALUE_COOL_MIN = "coolMin"
VALUE_COOL_MAX = "coolMax"

# System modes
SYSTEM_AUTO = "Auto"
SYSTEM_HEAT = "Heat"
SYSTEM_COOL = "Cool"
SYSTEM_OFF = "Off"

# Configuration keys
CONF_POLL_INTERVAL = "poll_interval"

# Update interval
DEFAULT_POLL_INTERVAL = 70  # seconds (1 minute 10 seconds) 