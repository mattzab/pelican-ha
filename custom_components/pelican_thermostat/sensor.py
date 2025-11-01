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
    # Measurement sensors
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
    # Status sensors
    {
        "key": "run_status",
        "name": "Run Status",
        "unit": None,
        "icon": "mdi:fan",
    },
    {
        "key": "status",
        "name": "Status",
        "unit": None,
        "icon": "mdi:information",
    },
    {
        "key": "set_by",
        "name": "Set By",
        "unit": None,
        "icon": "mdi:account",
    },
    {
        "key": "front_keypad",
        "name": "Front Keypad",
        "unit": None,
        "icon": "mdi:keyboard",
    },
    {
        "key": "aux_status",
        "name": "Aux Status",
        "unit": None,
        "icon": "mdi:electric-switch",
    },
    {
        "key": "status_display",
        "name": "Status Display",
        "unit": None,
        "icon": "mdi:text-box",
    },
    {
        "key": "schedule",
        "name": "Schedule",
        "unit": None,
        "icon": "mdi:calendar-clock",
    },
    # Fan sensor
    {
        "key": "fan",
        "name": "Fan Mode",
        "unit": None,
        "icon": "mdi:fan",
    },
    # System configuration sensors
    {
        "key": "heat_stages",
        "name": "Heat Stages",
        "unit": None,
        "icon": "mdi:fire",
    },
    {
        "key": "cool_stages",
        "name": "Cool Stages",
        "unit": None,
        "icon": "mdi:snowflake",
    },
    {
        "key": "fan_stages",
        "name": "Fan Stages",
        "unit": None,
        "icon": "mdi:fan",
    },
    {
        "key": "system_type",
        "name": "System Type",
        "unit": None,
        "icon": "mdi:hvac",
    },
    {
        "key": "temperature_format",
        "name": "Temperature Format",
        "unit": None,
        "icon": "mdi:thermometer",
    },
    {
        "key": "cycle_rate",
        "name": "Cycle Rate",
        "unit": None,
        "icon": "mdi:sync",
    },
    {
        "key": "anticipation_degrees",
        "name": "Anticipation Degrees",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "icon": "mdi:thermometer-chevron-up",
    },
    {
        "key": "calibration_offset",
        "name": "Calibration Offset",
        "unit": UnitOfTemperature.FAHRENHEIT,
        "icon": "mdi:thermometer-lines",
    },
    # Device info sensors
    {
        "key": "serial_no",
        "name": "Serial Number",
        "unit": None,
        "icon": "mdi:identifier",
    },
    {
        "key": "gateway",
        "name": "Gateway",
        "unit": None,
        "icon": "mdi:router-wireless",
    },
    {
        "key": "version",
        "name": "Version",
        "unit": None,
        "icon": "mdi:information-outline",
    },
    {
        "key": "install_date",
        "name": "Install Date",
        "unit": None,
        "icon": "mdi:calendar",
    },
    # Humidity control sensor
    {
        "key": "humidity_control",
        "name": "Humidity Control",
        "unit": None,
        "icon": "mdi:water-percent",
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

    _attr_has_entity_name = True

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
        
        self._attr_name = sensor_info['name']
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

 