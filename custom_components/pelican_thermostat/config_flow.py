"""Minimal config flow for Pelican Thermostat integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_BASE_URL,
    CONF_PASSWORD,
    CONF_POLL_INTERVAL,
    CONF_THERMOSTAT_NAME,
    CONF_USERNAME,
    DEFAULT_BASE_URL,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class PelicanThermostatConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Pelican Thermostat."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=f"Pelican Thermostat - {user_input[CONF_THERMOSTAT_NAME]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
                    vol.Required(CONF_THERMOSTAT_NAME): str,
                    vol.Optional(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): vol.All(
                        vol.Coerce(int), vol.Range(min=30, max=300)
                    ),
                }
            ),
        ) 