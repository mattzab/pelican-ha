"""Switch entities for Pelican Thermostat."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_THERMOSTAT_NAME,
    DOMAIN,
    KEYPAD_OFF,
    KEYPAD_ON,
    SCHEDULE_OFF,
    SCHEDULE_ON,
)
from .coordinator import PelicanThermostatCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pelican Thermostat switch entities."""
    coordinator: PelicanThermostatCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    entities = [
        PelicanScheduleSwitch(coordinator, config_entry),
        PelicanKeypadSwitch(coordinator, config_entry),
    ]

    async_add_entities(entities)


class PelicanScheduleSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Pelican Thermostat schedule switch."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: PelicanThermostatCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the schedule switch."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Schedule"
        self._attr_unique_id = f"{config_entry.entry_id}_schedule"
        self._attr_icon = "mdi:calendar-clock"

    @property
    def is_on(self) -> bool | None:
        """Return true if schedule is on."""
        data = self.coordinator.data
        schedule = data.get("schedule")
        return schedule == SCHEDULE_ON

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the schedule on."""
        await self.coordinator.set_schedule(SCHEDULE_ON)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the schedule off."""
        await self.coordinator.set_schedule(SCHEDULE_OFF)
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True


class PelicanKeypadSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Pelican Thermostat keypad lock switch."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: PelicanThermostatCoordinator, config_entry: ConfigEntry
    ) -> None:
        """Initialize the keypad switch."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_name = "Front Keypad"
        self._attr_unique_id = f"{config_entry.entry_id}_keypad"
        self._attr_icon = "mdi:keyboard"

    @property
    def is_on(self) -> bool | None:
        """Return true if keypad is enabled."""
        data = self.coordinator.data
        keypad = data.get("front_keypad")
        return keypad == KEYPAD_ON

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable the keypad."""
        await self.coordinator.set_keypad(KEYPAD_ON)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable the keypad (lock it)."""
        await self.coordinator.set_keypad(KEYPAD_OFF)
        await self.coordinator.async_request_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True
