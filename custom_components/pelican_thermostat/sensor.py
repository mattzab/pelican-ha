"""Sensor entities for Pelican Thermostat."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import PelicanThermostatCoordinator

SENSORS = [
    {
        "key": "temperature",
        "name": "Temperature",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "icon": "mdi:thermometer",
    },
    {
        "key": "humidity",
        "name": "Humidity",
        "unit": PERCENTAGE,
        "icon": "mdi:water-percent",
    },
    {
        "key": "co2_level",
        "name": "CO2 Level",
        "unit": "ppm",
        "icon": "mdi:molecule-co2",
    },
    {
        "key": "run_status",
        "name": "Run Status",
        "unit": None,
        "icon": "mdi:fan",
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Pelican Thermostat sensors."""
    coordinator: PelicanThermostatCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]

    entities = []
    for sensor in SENSORS:
        entities.append(
            PelicanThermostatSensor(coordinator, config_entry, sensor)
        )

    async_add_entities(entities)


class PelicanThermostatSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Pelican Thermostat sensor."""

    def __init__(
        self,
        coordinator: PelicanThermostatCoordinator,
        config_entry: ConfigEntry,
        sensor_info: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.sensor_info = sensor_info
        
        self._attr_name = f"{config_entry.data['thermostat_name']} {sensor_info['name']}"
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_info['key']}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_icon = sensor_info["icon"]

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        data = self.coordinator.data
        return data.get(self.sensor_info["key"])

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        # Consider available even if last update failed, as thermostat might be offline
        # but we still want to show last known values
        return True

 