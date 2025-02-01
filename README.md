# HassForge Incoming REST Integration

A Home Assistant integration that creates a configurable webhook endpoint to receive REST requests and store their data in a sensor entity.

## Features

- Creates a webhook endpoint with a customizable suffix for better organization
- Configurable allowed HTTP methods (GET, POST, OPTIONS, DELETE)
- Stores the latest request data in a sensor entity including:
  - Request content
  - HTTP method used
  - Headers
  - Query parameters
  - Request path
  - Content type
  - Timestamp

## Installation

1. Add this repository to HACS as a custom repository
2. Install the "HassForge Incoming REST" integration
3. Restart Home Assistant
4. Add the integration through the Home Assistant UI (Settings -> Devices & Services -> Add Integration)

## Configuration

When adding the integration, you'll need to configure:

1. Name - A name for your webhook endpoint (defaults to "HassForge Incoming REST")
2. Webhook Suffix - A custom suffix for your webhook URL (e.g., "my-device" will create a URL ending in "/my-device")
3. Allowed Methods - Select which HTTP methods are allowed (GET, POST, OPTIONS, DELETE)

## Usage

Once configured, the integration will:

1. Create a webhook URL in the format: `https://your-home-assistant/api/webhook/<webhook-id>/<webhook-suffix>`
2. Create a sensor entity that updates whenever the webhook receives a request
3. Store the latest request data in the sensor's attributes

The sensor's state will contain the request content (for POST requests) or indicate the request method for other types of requests.

### Example Sensor Data

The sensor will store the following attributes for each request:
```yaml
state: <request content or method>
attributes:
  method: POST
  headers: {...}
  query_params: {...}
  path: /api/webhook/xxx/my-device
  content_type: application/json
  timestamp: 2025-02-01T13:36:15
```

## Support

For issues and feature requests, please open an issue on GitHub.
