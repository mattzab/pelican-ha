"""Climate entity for Pelican Thermostat."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    CONF_NAME,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    CONF_THERMOSTAT_NAME,
    DOMAIN,
    FAN_AUTO,
    FAN_ON,
    STATUS_OCCUPIED,
    STATUS_VACANT,
    SYSTEM_AUTO,
    SYSTEM_COOL,
    SYSTEM_HEAT,
    SYSTEM_OFF,
)
from .coordinator import PelicanThermostatCoordinator

_LOGGER = logging.getLogger(__name__)

HVAC_MODE_MAP = {
    SYSTEM_OFF: HVACMode.OFF,
    SYSTEM_HEAT: HVACMode.HEAT,
    SYSTEM_COOL: HVACMode.COOL,
    SYSTEM_AUTO: HVACMode.AUTO,
}

HVAC_MODE_MAP_REVERSE = {v: k for k, v in HVAC_MODE_MAP.items()}

# Map Pelican fan modes to Home Assistant fan modes
FAN_MODE_MAP = {
    FAN_AUTO: "auto",
    FAN_ON: "on",
}

FAN_MODE_MAP_REVERSE = {v: k for k, v in FAN_MODE_MAP.items()}

# Preset modes for occupied/vacant status
PRESET_OCCUPIED = "occupied"
PRESET_VACANT = "vacant"

PRESET_MODE_MAP = {
    STATUS_OCCUPIED: PRESET_OCCUPIED,
    STATUS_VACANT: PRESET_VACANT,
}

PRESET_MODE_MAP_REVERSE = {v: k for k, v in PRESET_MODE_MAP.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pelican Thermostat climate entity."""
    coordinator: PelicanThermostatCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    async_add_entities([PelicanThermostatEntity(coordinator, config_entry)])


class PelicanThermostatEntity(CoordinatorEntity, ClimateEntity):
    """Representation of a Pelican Thermostat."""

    _attr_has_entity_name = True
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.PRESET_MODE
    )

    def __init__(
        self, coordinator: PelicanThermostatCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the thermostat."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = config_entry.data[CONF_THERMOSTAT_NAME]
        self._attr_unique_id = f"{config_entry.entry_id}_climate"
        self._attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
        self._attr_hvac_modes = list(HVAC_MODE_MAP.values())
        self._attr_target_temperature_step = 1.0
        self._attr_min_temp = 50.0
        self._attr_max_temp = 90.0
        self._attr_fan_modes = ["auto", "on"]
        self._attr_preset_modes = [PRESET_OCCUPIED, PRESET_VACANT]

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        data = self.coordinator.data
        return data.get("temperature")

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        data = self.coordinator.data
        if self.hvac_mode == HVACMode.HEAT:
            return data.get("heat_setting")
        if self.hvac_mode == HVACMode.COOL:
            return data.get("cool_setting")
        return None

    @property
    def target_temperature_high(self) -> float | None:
        """Return the high target temperature."""
        data = self.coordinator.data
        return data.get("cool_setting")

    @property
    def target_temperature_low(self) -> float | None:
        """Return the low target temperature."""
        data = self.coordinator.data
        return data.get("heat_setting")

    @property
    def hvac_mode(self) -> HVACMode:
        """Return the current HVAC mode."""
        data = self.coordinator.data
        system_mode = data.get("system_mode")
        if system_mode is None and not self.coordinator.last_update_success:
            # If we can't get the mode and last update failed, assume offline
            return HVACMode.OFF
        return HVAC_MODE_MAP.get(system_mode, HVACMode.OFF)

    @property
    def run_status(self) -> str | None:
        """Return the current run status."""
        data = self.coordinator.data
        return data.get("run_status")

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            temperature = kwargs[ATTR_TEMPERATURE]
            if self.hvac_mode == HVACMode.HEAT:
                await self.coordinator.set_heat_setting(temperature)
            elif self.hvac_mode == HVACMode.COOL:
                await self.coordinator.set_cool_setting(temperature)

        # Handle temperature range for AUTO mode
        if self.hvac_mode == HVACMode.AUTO:
            if "target_temp_high" in kwargs:
                await self.coordinator.set_cool_setting(kwargs["target_temp_high"])
            if "target_temp_low" in kwargs:
                await self.coordinator.set_heat_setting(kwargs["target_temp_low"])

        await self.coordinator.async_request_refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        system_mode = HVAC_MODE_MAP_REVERSE.get(hvac_mode, SYSTEM_OFF)
        await self.coordinator.set_system_mode(system_mode)
        await self.coordinator.async_request_refresh()

    @property
    def fan_mode(self) -> str | None:
        """Return the current fan mode."""
        data = self.coordinator.data
        pelican_fan_mode = data.get("fan_mode")
        return FAN_MODE_MAP.get(pelican_fan_mode)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new fan mode."""
        pelican_fan_mode = FAN_MODE_MAP_REVERSE.get(fan_mode)
        if pelican_fan_mode:
            await self.coordinator.set_fan_mode(pelican_fan_mode)
            await self.coordinator.async_request_refresh()

    @property
    def preset_mode(self) -> str | None:
        """Return the current preset mode."""
        data = self.coordinator.data
        status = data.get("status")
        return PRESET_MODE_MAP.get(status)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        pelican_status = PRESET_MODE_MAP_REVERSE.get(preset_mode)
        if pelican_status:
            # Note: Setting status might not be directly supported by API
            # This would require further investigation of API capabilities
            _LOGGER.warning("Setting preset mode is not yet fully implemented")

    @property
    def hvac_action(self) -> HVACAction | None:
        """Return the current HVAC action (heating, cooling, idle, etc)."""
        data = self.coordinator.data
        run_status = data.get("run_status")
        
        if not run_status:
            return HVACAction.IDLE
        
        run_status_lower = run_status.lower()
        
        # Map run status to HVAC actions
        if "heat" in run_status_lower:
            return HVACAction.HEATING
        elif "cool" in run_status_lower:
            return HVACAction.COOLING
        elif "fan" in run_status_lower:
            return HVACAction.FAN
        elif "idle" in run_status_lower or "off" in run_status_lower:
            return HVACAction.IDLE
        
        # Default to idle if we can't determine
        return HVACAction.IDLE


    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Consider available even if last update failed, as thermostat might be offline
        # but we still want to allow control attempts
        return True

 