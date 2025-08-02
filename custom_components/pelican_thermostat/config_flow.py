"""Config flow for Pelican Thermostat integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_BASE_URL,
    CONF_POLL_INTERVAL,
    CONF_THERMOSTAT_NAME,
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
        errors = {}

        if user_input is not None:
            try:
                # Test the connection
                await self._test_connection(user_input)
                
                return self.async_create_entry(
                    title=f"Pelican Thermostat - {user_input[CONF_THERMOSTAT_NAME]}",
                    data=user_input,
                )
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "cannot_connect"

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
            errors=errors,
        )

    async def _test_connection(self, user_input: dict[str, Any]) -> None:
        """Test the connection to the API."""
        # This is a placeholder for connection testing
        # You may want to implement actual API testing here
        _LOGGER.info("Testing connection to Pelican Thermostat API")
        # For now, we'll assume the connection is successful
        # In a real implementation, you would make an API call here 