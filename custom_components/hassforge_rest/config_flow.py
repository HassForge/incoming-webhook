"""Config flow for HassForge Incoming REST integration."""
from __future__ import annotations

import secrets
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_NAME,
    CONF_WEBHOOK_ID,
    CONF_WEBHOOK_SUFFIX,
    CONF_ALLOWED_METHODS,
    DEFAULT_NAME,
    DEFAULT_ALLOWED_METHODS,
    DOMAIN,
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HassForge Incoming REST."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                        vol.Required(CONF_WEBHOOK_SUFFIX): str,
                        vol.Required(CONF_ALLOWED_METHODS, default=DEFAULT_ALLOWED_METHODS): cv.multi_select(DEFAULT_ALLOWED_METHODS),
                    }
                ),
            )

        webhook_id = secrets.token_hex(32)
        user_input[CONF_WEBHOOK_ID] = webhook_id

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input,
        )
