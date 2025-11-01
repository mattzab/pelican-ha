"""The Pelican Thermostat integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import PelicanThermostatCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.NUMBER,
]


# No async_setup needed for config flow integrations


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pelican Thermostat from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = PelicanThermostatCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Ensure the coordinator is properly set up for polling
    # The coordinator will automatically start polling when entities are added
    _LOGGER.info("Coordinator setup complete, update_interval: %s", coordinator.update_interval)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok 