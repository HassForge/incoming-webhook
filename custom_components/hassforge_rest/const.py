"""Constants for the HassForge Incoming REST integration."""
from typing import Final

DOMAIN: Final = "hassforge_rest"
DEFAULT_NAME: Final = "HassForge Incoming REST"

CONF_WEBHOOK_ID: Final = "webhook_id"
CONF_WEBHOOK_URL: Final = "webhook_url"
CONF_WEBHOOK_SUFFIX: Final = "webhook_suffix"
CONF_ALLOWED_METHODS: Final = "allowed_methods"

# Configuration and options
CONF_NAME: Final = "name"
CONF_DEVICE_ID: Final = "device_id"

PLATFORMS: Final = ["sensor"]

DEFAULT_ALLOWED_METHODS: Final = ["GET", "POST", "OPTIONS", "DELETE"]

ATTR_METHOD: Final = "method"
ATTR_HEADERS: Final = "headers"
ATTR_QUERY_PARAMS: Final = "query_params"
ATTR_PATH: Final = "path"
ATTR_CONTENT_TYPE: Final = "content_type"
ATTR_TIMESTAMP: Final = "timestamp"
