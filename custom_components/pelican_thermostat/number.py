"""Number entities for Pelican Thermostat."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_THERMOSTAT_NAME, DOMAIN
from .coordinator import PelicanThermostatCoordinator

_LOGGER = logging.getLogger(__name__)

# Define number entities configuration
NUMBER_ENTITIES = [
    {
        "key": "humidify_setting",
        "name": "Humidify Setpoint",
        "icon": "mdi:water-plus",
        "unit": "%",
        "min": 0,
        "max": 100,
        "step": 1,
        "setter": "set_humidify_setting",
    },
    {
        "key": "dehumidify_setting",
        "name": "Dehumidify Setpoint",
        "icon": "mdi:water-minus",
        "unit": "%",
        "min": 0,
        "max": 100,
        "step": 1,
        "setter": "set_dehumidify_setting",
    },
    {
        "key": "co2_setting",
        "name": "CO2 Setpoint",
        "icon": "mdi:molecule-co2",
        "unit": "ppm",
        "min": 0,
        "max": 2000,
        "step": 50,
        "setter": "set_co2_setting",
    },
    {
        "key": "min_heat_setting",
        "name": "Min Heat Setting",
        "icon": "mdi:thermometer-low",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "min": 40,
        "max": 90,
        "step": 1,
        "setter": "set_min_heat_setting",
    },
    {
        "key": "max_heat_setting",
        "name": "Max Heat Setting",
        "icon": "mdi:thermometer-high",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "min": 40,
        "max": 90,
        "step": 1,
        "setter": "set_max_heat_setting",
    },
    {
        "key": "min_cool_setting",
        "name": "Min Cool Setting",
        "icon": "mdi:thermometer-low",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "min": 40,
        "max": 90,
        "step": 1,
        "setter": "set_min_cool_setting",
    },
    {
        "key": "max_cool_setting",
        "name": "Max Cool Setting",
        "icon": "mdi:thermometer-high",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "min": 40,
        "max": 90,
        "step": 1,
        "setter": "set_max_cool_setting",
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pelican Thermostat number entities."""
    coordinator: PelicanThermostatCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    entities = []
    for entity_info in NUMBER_ENTITIES:
        entities.append(
            PelicanThermostatNumber(coordinator, config_entry, entity_info)
        )

    async_add_entities(entities)


class PelicanThermostatNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Pelican Thermostat number entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PelicanThermostatCoordinator,
        config_entry: ConfigEntry,
        entity_info: dict,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_info = entity_info

        self._attr_name = entity_info["name"]
        self._attr_unique_id = f"{config_entry.entry_id}_{entity_info['key']}"
        self._attr_icon = entity_info["icon"]
        self._attr_native_unit_of_measurement = entity_info["unit"]
        self._attr_native_min_value = entity_info["min"]
        self._attr_native_max_value = entity_info["max"]
        self._attr_native_step = entity_info["step"]

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        data = self.coordinator.data
        return data.get(self.entity_info["key"])

    async def async_set_native_value(self, value: float) -> None:
        """Set the new value."""
        setter_method = self.entity_info["setter"]
        setter = getattr(self.coordinator, setter_method, None)
        
        if setter is None:
            _LOGGER.error(
                "Setter method %s not found on coordinator", setter_method
            )
            return

        try:
            await setter(value)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error(
                "Failed to set %s to %s: %s",
                self.entity_info["name"],
                value,
                err,
            )

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True
