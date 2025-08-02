"""Data coordinator for Pelican Thermostat."""
from __future__ import annotations

import asyncio
import logging
import xml.etree.ElementTree as ET
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
    VALUE_CO2_LEVEL,
    VALUE_HUMIDITY,
    VALUE_TEMPERATURE,
)

_LOGGER = logging.getLogger(__name__)


class PelicanThermostatCoordinator(DataUpdateCoordinator):
    """Data coordinator for Pelican Thermostat."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        poll_interval = entry.data.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name="Pelican Thermostat",
            update_interval=poll_interval,
        )
        self.entry = entry
        self.base_url = entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]
        self.thermostat_name = entry.data[CONF_THERMOSTAT_NAME]

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            async with async_timeout.timeout(15):  # Increased timeout for offline thermostats
                return await self._fetch_thermostat_data()
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout fetching thermostat data (thermostat may be offline)")
            # Return last known data instead of failing completely
            return self.data if self.data else {}
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def _fetch_thermostat_data(self) -> dict[str, Any]:
        """Fetch thermostat data from API."""
        # Get basic sensor data
        params = {
            API_USERNAME: self.username,
            API_PASSWORD: self.password,
            API_REQUEST: REQUEST_GET,
            API_OBJECT: OBJECT_THERMOSTAT,
            API_SELECTION: f"name:{self.thermostat_name};",
            API_VALUE: f"{VALUE_TEMPERATURE};{VALUE_HUMIDITY};{VALUE_CO2_LEVEL}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                response.raise_for_status()
                data = await response.text()
                _LOGGER.debug("API response: %s", data)
                
                result = self._parse_thermostat_data(data)
                
                # Try to get additional system information
                # Note: These might not be available if thermostat is offline
                try:
                    # Try to get system mode
                    system_params = params.copy()
                    system_params[API_VALUE] = "system"
                    async with session.get(self.base_url, params=system_params, timeout=aiohttp.ClientTimeout(total=10)) as system_response:
                        if system_response.status == 200:
                            system_data = await system_response.text()
                            system_result = self._parse_system_data(system_data)
                            result.update(system_result)
                except asyncio.TimeoutError:
                    _LOGGER.debug("Timeout fetching system data (thermostat may be offline)")
                except Exception as err:
                    _LOGGER.debug("Could not fetch system data: %s", err)
                
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
            
            # Parse temperature
            temp_elem = thermostat_elem.find("temperature")
            if temp_elem is not None and temp_elem.text:
                try:
                    result["temperature"] = float(temp_elem.text)
                except ValueError:
                    _LOGGER.warning("Invalid temperature value: %s", temp_elem.text)
            
            # Parse humidity
            humidity_elem = thermostat_elem.find("humidity")
            if humidity_elem is not None and humidity_elem.text:
                try:
                    result["humidity"] = float(humidity_elem.text)
                except ValueError:
                    _LOGGER.warning("Invalid humidity value: %s", humidity_elem.text)
            
            # Parse CO2 level
            co2_elem = thermostat_elem.find("co2Level")
            if co2_elem is not None and co2_elem.text:
                try:
                    result["co2_level"] = int(co2_elem.text)
                except ValueError:
                    _LOGGER.warning("Invalid CO2 level value: %s", co2_elem.text)
            
            # For now, we'll need to make additional API calls to get system mode and setpoints
            # These might not be available in the current API response
            result["system_mode"] = None
            result["heat_setting"] = None
            result["cool_setting"] = None
            
            return result
            
        except ET.ParseError as err:
            _LOGGER.error("Failed to parse XML response: %s", err)
            return {}
        except Exception as err:
            _LOGGER.error("Error parsing thermostat data: %s", err)
            return {}
    
    def _parse_system_data(self, data: str) -> dict[str, Any]:
        """Parse system data from API response."""
        try:
            root = ET.fromstring(data)
            
            # Check if the request was successful
            success_elem = root.find("success")
            if success_elem is None or success_elem.text != "1":
                return {}
            
            # Parse thermostat data
            thermostat_elem = root.find("Thermostat")
            if thermostat_elem is None:
                return {}
            
            result = {}
            
            # Parse system mode
            system_elem = thermostat_elem.find("system")
            if system_elem is not None and system_elem.text:
                result["system_mode"] = system_elem.text
            
            # Parse heat setting
            heat_elem = thermostat_elem.find("heatSetting")
            if heat_elem is not None and heat_elem.text:
                try:
                    result["heat_setting"] = float(heat_elem.text)
                except ValueError:
                    _LOGGER.warning("Invalid heat setting value: %s", heat_elem.text)
            
            # Parse cool setting
            cool_elem = thermostat_elem.find("coolSetting")
            if cool_elem is not None and cool_elem.text:
                try:
                    result["cool_setting"] = float(cool_elem.text)
                except ValueError:
                    _LOGGER.warning("Invalid cool setting value: %s", cool_elem.text)
            
            return result
            
        except ET.ParseError as err:
            _LOGGER.debug("Failed to parse system XML response: %s", err)
            return {}
        except Exception as err:
            _LOGGER.debug("Error parsing system data: %s", err)
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