"""The Pelican Thermostat integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries

from .const import (
    CONF_BASE_URL,
    CONF_PASSWORD,
    CONF_POLL_INTERVAL,
    CONF_THERMOSTAT_NAME,
    CONF_USERNAME,
    DEFAULT_BASE_URL,
    DOMAIN,
)
from .coordinator import PelicanThermostatCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.CLIMATE, Platform.SENSOR]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): cv.string,
                vol.Required(CONF_THERMOSTAT_NAME): cv.string,
                vol.Optional(CONF_POLL_INTERVAL, default=70): vol.All(
                    vol.Coerce(int), vol.Range(min=30, max=300)
                ),
            }
        )
    }
)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Pelican Thermostat component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pelican Thermostat from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = PelicanThermostatCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok 