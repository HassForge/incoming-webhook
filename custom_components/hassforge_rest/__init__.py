"""The HassForge Incoming REST integration."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import web
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_WEBHOOK_ID,
    CONF_WEBHOOK_URL,
    CONF_WEBHOOK_SUFFIX,
    CONF_ALLOWED_METHODS,
    DOMAIN,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HassForge Incoming REST component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HassForge Incoming REST from a config entry."""
    webhook_id = entry.data[CONF_WEBHOOK_ID]
    webhook_suffix = entry.data[CONF_WEBHOOK_SUFFIX]
    allowed_methods = entry.data[CONF_ALLOWED_METHODS]

    webhook_url = f"{hass.config.external_url}/api/webhook/{webhook_id}/{webhook_suffix}"
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_WEBHOOK_URL: webhook_url,
        CONF_WEBHOOK_ID: webhook_id,
        CONF_WEBHOOK_SUFFIX: webhook_suffix,
        CONF_ALLOWED_METHODS: allowed_methods,
    }

    async def handle_webhook(hass: HomeAssistant, webhook_id: str, request: web.Request):
        """Handle webhook callback."""
        try:
            # Check if the method is allowed
            if request.method not in allowed_methods:
                return web.Response(
                    text=f"Method {request.method} not allowed",
                    status=405,
                )

            # Get the sensor entity
            sensor = next(
                (
                    entity
                    for entity in hass.data[DOMAIN].get("entities", [])
                    if entity.unique_id == f"{entry.entry_id}_webhook"
                ),
                None,
            )

            if not sensor:
                _LOGGER.error("Sensor entity not found")
                return web.Response(text="Internal error", status=500)

            # Process the request
            headers = dict(request.headers)
            query_params = dict(request.query)
            path = request.path

            # Get content based on method
            content = None
            content_type = headers.get("content-type")

            if request.method == "POST":
                if "application/json" in content_type:
                    content = await request.json()
                elif "application/x-www-form-urlencoded" in content_type:
                    content = await request.post()
                else:
                    content = await request.text()

            # Update the sensor
            sensor.update_from_webhook(
                content,
                request.method,
                headers,
                query_params,
                path,
                content_type,
            )

            return web.Response(text="Success", status=200)

        except Exception as ex:
            _LOGGER.error("Error processing webhook: %s", ex)
            return web.Response(text="Error", status=500)

    hass.components.webhook.async_register(
        DOMAIN, entry.data[CONF_NAME], webhook_id, handle_webhook
    )

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    webhook_id = entry.data[CONF_WEBHOOK_ID]
    hass.components.webhook.async_unregister(webhook_id)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
