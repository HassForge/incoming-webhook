"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_CONTENT_TYPE,
    ATTR_HEADERS,
    ATTR_METHOD,
    ATTR_PATH,
    ATTR_QUERY_PARAMS,
    ATTR_TIMESTAMP,
    ATTR_WEBHOOK_URL,
    CONF_NAME,
    CONF_WEBHOOK_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    name = config_entry.data[CONF_NAME]
    sensor = WebhookSensor(hass, config_entry.entry_id, name)
    async_add_entities([sensor], True)


class WebhookSensor(SensorEntity):
    """Representation of a Webhook Sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry_id: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry_id = entry_id
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_webhook"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {
            ATTR_METHOD: None,
            ATTR_HEADERS: {},
            ATTR_QUERY_PARAMS: {},
            ATTR_PATH: None,
            ATTR_CONTENT_TYPE: None,
            ATTR_TIMESTAMP: None,
            ATTR_WEBHOOK_URL: None,
        }

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        if self._entry_id in self.hass.data[DOMAIN]:
            self._attr_extra_state_attributes[ATTR_WEBHOOK_URL] = (
                self.hass.data[DOMAIN][self._entry_id][CONF_WEBHOOK_URL]
            )

    def update_from_webhook(
        self,
        value: StateType,
        method: str,
        headers: dict,
        query_params: dict,
        path: str,
        content_type: str | None = None,
    ) -> None:
        """Update sensor from webhook data."""
        self._attr_native_value = value
        self._attr_extra_state_attributes.update({
            ATTR_METHOD: method,
            ATTR_HEADERS: headers,
            ATTR_QUERY_PARAMS: query_params,
            ATTR_PATH: path,
            ATTR_CONTENT_TYPE: content_type,
            ATTR_TIMESTAMP: datetime.now().isoformat(),
        })
        self.schedule_update_ha_state()
