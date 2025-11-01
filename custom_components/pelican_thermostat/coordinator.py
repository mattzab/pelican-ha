"""Data coordinator for Pelican Thermostat."""
from __future__ import annotations

import asyncio
import logging
import xml.etree.ElementTree as ET
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    API_OBJECT,
    API_PASSWORD,
    API_REQUEST,
    API_SELECTION,
    API_USERNAME,
    API_VALUE,
    CONF_BASE_URL,
    CONF_PASSWORD,
    CONF_POLL_INTERVAL,
    CONF_THERMOSTAT_NAME,
    CONF_USERNAME,
    DEFAULT_BASE_URL,
    DEFAULT_POLL_INTERVAL,
    OBJECT_THERMOSTAT,
    REQUEST_GET,
    REQUEST_SET,
    VALUE_ANTICIPATION_DEGREES,
    VALUE_AUX_STATUS,
    VALUE_CALIBRATION_OFFSET,
    VALUE_CO2_LEVEL,
    VALUE_CO2_SETTING,
    VALUE_COOL_STAGES,
    VALUE_CYCLE_RATE,
    VALUE_DEHUMIDIFY_SETTING,
    VALUE_FAN,
    VALUE_FAN_STAGES,
    VALUE_FRONT_KEYPAD,
    VALUE_GATEWAY,
    VALUE_HEAT_STAGES,
    VALUE_HUMIDIFY_SETTING,
    VALUE_HUMIDITY,
    VALUE_HUMIDITY_CONTROL,
    VALUE_INSTALL_DATE,
    VALUE_MAX_COOL_SETTING,
    VALUE_MAX_HEAT_SETTING,
    VALUE_MAX_SAFE_TEMP,
    VALUE_MIN_COOL_SETTING,
    VALUE_MIN_HEAT_SETTING,
    VALUE_MIN_SAFE_TEMP,
    VALUE_NOTIFICATION_SENSITIVITY,
    VALUE_NOTIFICATION_SETPOINT,
    VALUE_NOTIFICATION_UNREACHABLE,
    VALUE_RUN_STATUS,
    VALUE_SCHEDULE,
    VALUE_SERIAL_NO,
    VALUE_SET_BY,
    VALUE_STATUS,
    VALUE_STATUS_DISPLAY,
    VALUE_SYSTEM_TYPE,
    VALUE_TEMPERATURE,
    VALUE_TEMPERATURE_FORMAT,
    VALUE_VERSION,
)

_LOGGER = logging.getLogger(__name__)


class PelicanThermostatCoordinator(DataUpdateCoordinator):
    """Data coordinator for Pelican Thermostat."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        # Check options first, fall back to data, then default
        poll_interval = entry.options.get(
            CONF_POLL_INTERVAL,
            entry.data.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)
        )
        _LOGGER.info("Initializing coordinator with poll interval: %s seconds", poll_interval)
        super().__init__(
            hass,
            _LOGGER,
            name="Pelican Thermostat",
            update_interval=timedelta(seconds=poll_interval),
        )
        self.entry = entry
        self.base_url = entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]
        self.thermostat_name = entry.data[CONF_THERMOSTAT_NAME]
        _LOGGER.info("Coordinator initialized with update_interval: %s", self.update_interval)

    def update_poll_interval(self) -> None:
        """Update the poll interval from config entry options."""
        poll_interval = self.entry.options.get(
            CONF_POLL_INTERVAL,
            self.entry.data.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)
        )
        new_interval = timedelta(seconds=poll_interval)
        if self.update_interval != new_interval:
            _LOGGER.info("Updating poll interval from %s to %s", self.update_interval, new_interval)
            self.update_interval = new_interval

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        _LOGGER.info("Polling thermostat data...")
        try:
            async with async_timeout.timeout(15):  # Increased timeout for offline thermostats
                result = await self._fetch_thermostat_data()
                _LOGGER.info("Successfully polled thermostat data")
                return result
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout fetching thermostat data (thermostat may be offline)")
            # Return last known data instead of failing completely
            return self.data if self.data else {}
        except Exception as err:
            _LOGGER.error("Error polling thermostat data: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _fetch_thermostat_data(self) -> dict[str, Any]:
        """Fetch thermostat data from API."""
        # Get all data in a single request to improve performance
        # Build comprehensive value list for all attributes
        value_list = [
            # Measurements
            VALUE_TEMPERATURE, VALUE_HUMIDITY, VALUE_CO2_LEVEL, VALUE_RUN_STATUS,
            # System and settings
            "system", "heatSetting", "coolSetting", VALUE_SCHEDULE, VALUE_FAN,
            # Status
            VALUE_STATUS, VALUE_SET_BY, VALUE_FRONT_KEYPAD, VALUE_AUX_STATUS, VALUE_STATUS_DISPLAY,
            # Humidity control
            VALUE_HUMIDIFY_SETTING, VALUE_DEHUMIDIFY_SETTING, VALUE_HUMIDITY_CONTROL,
            # CO2 control
            VALUE_CO2_SETTING,
            # System configuration
            VALUE_HEAT_STAGES, VALUE_COOL_STAGES, VALUE_FAN_STAGES, VALUE_SYSTEM_TYPE,
            VALUE_TEMPERATURE_FORMAT, VALUE_CYCLE_RATE, VALUE_ANTICIPATION_DEGREES, VALUE_CALIBRATION_OFFSET,
            # Temperature limits
            VALUE_MIN_HEAT_SETTING, VALUE_MAX_HEAT_SETTING, VALUE_MIN_COOL_SETTING, VALUE_MAX_COOL_SETTING,
            VALUE_MIN_SAFE_TEMP, VALUE_MAX_SAFE_TEMP,
            # Device info
            VALUE_SERIAL_NO, VALUE_GATEWAY, VALUE_VERSION, VALUE_INSTALL_DATE,
            # Notification settings
            VALUE_NOTIFICATION_SENSITIVITY, VALUE_NOTIFICATION_SETPOINT, VALUE_NOTIFICATION_UNREACHABLE,
        ]
        
        params = {
            API_USERNAME: self.username,
            API_PASSWORD: self.password,
            API_REQUEST: REQUEST_GET,
            API_OBJECT: OBJECT_THERMOSTAT,
            API_SELECTION: f"name:{self.thermostat_name};",
            API_VALUE: ";".join(value_list),
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                response.raise_for_status()
                data = await response.text()
                _LOGGER.debug("API response: %s", data)
                
                result = self._parse_thermostat_data(data)
                
                return result

    def _parse_thermostat_data(self, data: str) -> dict[str, Any]:
        """Parse thermostat data from API response."""
        try:
            root = ET.fromstring(data)
            
            # Check if the request was successful
            success_elem = root.find("success")
            if success_elem is None or success_elem.text != "1":
                _LOGGER.error("API request was not successful")
                return {}
            
            # Parse thermostat data
            thermostat_elem = root.find("Thermostat")
            if thermostat_elem is None:
                _LOGGER.error("No thermostat data found in response")
                return {}
            
            result = {}
            
            # Helper function to parse elements
            def parse_float(tag: str, key: str = None) -> None:
                key = key or tag.replace("_", "_").lower()
                elem = thermostat_elem.find(tag)
                if elem is not None and elem.text:
                    try:
                        result[key] = float(elem.text)
                    except ValueError:
                        _LOGGER.warning("Invalid %s value: %s", tag, elem.text)
            
            def parse_int(tag: str, key: str = None) -> None:
                key = key or tag.replace("_", "_").lower()
                elem = thermostat_elem.find(tag)
                if elem is not None and elem.text:
                    try:
                        result[key] = int(elem.text)
                    except ValueError:
                        _LOGGER.warning("Invalid %s value: %s", tag, elem.text)
            
            def parse_string(tag: str, key: str = None) -> None:
                key = key or tag.replace("_", "_").lower()
                elem = thermostat_elem.find(tag)
                result[key] = elem.text if elem is not None and elem.text else None
            
            # Parse measurements
            parse_float("temperature")
            parse_float("humidity")
            parse_int("co2Level", "co2_level")
            parse_string("runStatus", "run_status")
            
            # Parse system and settings
            parse_string("system", "system_mode")
            parse_float("heatSetting", "heat_setting")
            parse_float("coolSetting", "cool_setting")
            parse_string("schedule")
            parse_string("fan", "fan_mode")
            
            # Parse status
            parse_string("status")
            parse_string("setBy", "set_by")
            parse_string("frontKeypad", "front_keypad")
            parse_string("auxStatus", "aux_status")
            parse_string("statusDisplay", "status_display")
            
            # Parse humidity control
            parse_int("humidifySetting", "humidify_setting")
            parse_int("dehumidifySetting", "dehumidify_setting")
            parse_string("humidityControl", "humidity_control")
            
            # Parse CO2 control
            parse_int("co2Setting", "co2_setting")
            
            # Parse system configuration
            parse_int("heatStages", "heat_stages")
            parse_int("coolStages", "cool_stages")
            parse_int("fanStages", "fan_stages")
            parse_string("systemType", "system_type")
            parse_string("temperatureFormat", "temperature_format")
            parse_int("cycleRate", "cycle_rate")
            parse_float("anticipationDegrees", "anticipation_degrees")
            parse_float("calibrationOffset", "calibration_offset")
            
            # Parse temperature limits
            parse_int("minHeatSetting", "min_heat_setting")
            parse_int("maxHeatSetting", "max_heat_setting")
            parse_int("minCoolSetting", "min_cool_setting")
            parse_int("maxCoolSetting", "max_cool_setting")
            parse_int("minSafeTemp", "min_safe_temp")
            parse_int("maxSafeTemp", "max_safe_temp")
            
            # Parse device info
            parse_string("serialNo", "serial_no")
            parse_string("gateway")
            parse_string("version")
            parse_string("installDate", "install_date")
            
            # Parse notification settings
            parse_string("notificationSensitivity", "notification_sensitivity")
            parse_int("notificationSetpoint", "notification_setpoint")
            parse_string("notificationUnreachable", "notification_unreachable")
            
            return result
            
        except ET.ParseError as err:
            _LOGGER.error("Failed to parse XML response: %s", err)
            return {}
        except Exception as err:
            _LOGGER.error("Error parsing thermostat data: %s", err)
            return {}
            
    async def set_system_mode(self, mode: str) -> bool:
        """Set the system mode."""
        return await self._set_thermostat_value("system", mode)

    async def set_heat_setting(self, temperature: float) -> bool:
        """Set the heating setpoint."""
        return await self._set_thermostat_value("heatSetting", str(temperature))

    async def set_cool_setting(self, temperature: float) -> bool:
        """Set the cooling setpoint."""
        return await self._set_thermostat_value("coolSetting", str(temperature))

    async def set_fan_mode(self, mode: str) -> bool:
        """Set the fan mode (Auto/On)."""
        return await self._set_thermostat_value("fan", mode)

    async def set_schedule(self, value: str) -> bool:
        """Set the schedule (On/Off or schedule name)."""
        return await self._set_thermostat_value("schedule", value)

    async def set_keypad(self, value: str) -> bool:
        """Set the front keypad status (On/Off)."""
        return await self._set_thermostat_value("frontKeypad", value)

    async def set_humidify_setting(self, value: int) -> bool:
        """Set the humidify setpoint."""
        return await self._set_thermostat_value("humidifySetting", str(value))

    async def set_dehumidify_setting(self, value: int) -> bool:
        """Set the dehumidify setpoint."""
        return await self._set_thermostat_value("dehumidifySetting", str(value))

    async def set_co2_setting(self, value: int) -> bool:
        """Set the CO2 setpoint."""
        return await self._set_thermostat_value("co2Setting", str(value))

    async def set_min_heat_setting(self, value: int) -> bool:
        """Set the minimum heat setting."""
        return await self._set_thermostat_value("minHeatSetting", str(value))

    async def set_max_heat_setting(self, value: int) -> bool:
        """Set the maximum heat setting."""
        return await self._set_thermostat_value("maxHeatSetting", str(value))

    async def set_min_cool_setting(self, value: int) -> bool:
        """Set the minimum cool setting."""
        return await self._set_thermostat_value("minCoolSetting", str(value))

    async def set_max_cool_setting(self, value: int) -> bool:
        """Set the maximum cool setting."""
        return await self._set_thermostat_value("maxCoolSetting", str(value))

    async def _set_thermostat_value(self, value_type: str, value: str) -> bool:
        """Set a thermostat value via API."""
        params = {
            API_USERNAME: self.username,
            API_PASSWORD: self.password,
            API_REQUEST: REQUEST_SET,
            API_OBJECT: OBJECT_THERMOSTAT,
            API_SELECTION: f"name:{self.thermostat_name};",
            API_VALUE: f"{value_type}:{value}",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=aiohttp.ClientTimeout(total=20)) as response:
                    response.raise_for_status()
                    response_text = await response.text()
                    _LOGGER.debug("Set value response: %s", response_text)
                    
                    # Parse the response to check if it was successful
                    try:
                        root = ET.fromstring(response_text)
                        success_elem = root.find("success")
                        if success_elem is not None and success_elem.text == "1":
                            _LOGGER.info("Successfully set %s to %s", value_type, value)
                            return True
                        else:
                            _LOGGER.error("Failed to set %s to %s", value_type, value)
                            return False
                    except ET.ParseError:
                        _LOGGER.warning("Could not parse SET response, assuming success")
                        return True
                        
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout setting %s to %s (thermostat may be offline or disconnected)", value_type, value)
            return True  # Assume success for timeouts - thermostat may be offline
        except Exception as err:
            _LOGGER.error("Error setting thermostat value %s to %s: %s", value_type, value, err)
            return False 