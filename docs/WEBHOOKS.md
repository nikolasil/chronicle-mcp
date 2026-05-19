# Webhooks Guide

ChronicleMCP supports webhooks for notifying external systems about browser history events.

## Overview

Webhooks allow external services to receive real-time notifications when:
- New history entries are added
- History entries are deleted
- Bookmarks are added or removed
- Downloads are recorded

## Webhook Configuration

### Basic Setup

Webhooks are configured in `chronicle-mcp.toml`:

```toml
[webhooks]
enabled = true
max_retries = 3
retry_delay = 1.0
timeout = 10.0
```

### Security

Configure webhook secrets for payload verification:

```toml
[webhooks.secrets]
my_webhook = "your-secret-token-here"
```

## Registering Webhooks

### Using the Python API

```python
from chronicle_mcp.webhooks import get_webhook_manager

manager = get_webhook_manager()

# Register a webhook
webhook_id = manager.register_webhook(
    url="https://example.com/webhook",
    event_types=["history_added", "history_deleted"],
    secret="optional-secret"
)

print(f"Registered webhook: {webhook_id}")
```

### Event Types

| Event Type | Description |
|------------|-------------|
| `history_added` | New history entry added |
| `history_deleted` | History entry deleted |
| `bookmark_added` | Bookmark added |
| `bookmark_deleted` | Bookmark removed |
| `download_added` | Download recorded |

## Webhook Payload

When an event triggers, the webhook receives a POST request with:

```json
{
  "event_type": "history_added",
  "browser": "chrome",
  "timestamp": "2024-01-15T14:22:00Z",
  "data": {
    "url": "https://example.com/page",
    "title": "Example Page",
    "visit_count": 1
  }
}
```

### With Secret Signature

If a secret is configured, the request includes a signature header:

```
X-Webhook-Signature: sha256=abc123...
```

Verify the signature:

```python
import hmac
import hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Webhook Management

### List Webhooks

```python
manager = get_webhook_manager()
webhooks = manager.list_webhooks()

for webhook in webhooks:
    print(f"ID: {webhook.id}")
    print(f"URL: {webhook.url}")
    print(f"Events: {webhook.event_types}")
```

### Get Specific Webhook

```python
webhook = manager.get_webhook(webhook_id)
if webhook:
    print(f"URL: {webhook.url}")
```

### Unregister Webhook

```python
success = manager.unregister_webhook(webhook_id)
if success:
    print("Webhook removed")
```

### Trigger Event Manually

```python
from chronicle_mcp.webhooks import WebhookEvent

event = WebhookEvent(
    event_type="history_added",
    browser="chrome",
    timestamp="2024-01-15T14:22:00Z",
    data={"url": "https://example.com"}
)

triggered = manager.trigger_event(event)
print(f"Triggered {triggered} webhooks")
```

## Starting the Webhook Worker

The webhook worker processes events asynchronously:

```python
manager = get_webhook_manager()
manager.start()

# Do work...

manager.stop()
```

### With Start/Stop Lifecycle

```python
manager = get_webhook_manager()

try:
    manager.start()
    # Webhooks will be processed
finally:
    manager.stop()
```

## HTTP API Endpoints

### Register Webhook

```
POST /api/webhooks
Content-Type: application/json

{
  "url": "https://example.com/webhook",
  "event_types": ["history_added"],
  "secret": "optional-secret"
}
```

### List Webhooks

```
GET /api/webhooks
```

### Delete Webhook

```
DELETE /api/webhooks/{webhook_id}
```

## Retry Behavior

Failed webhook deliveries are retried up to `max_retries` times:

1. First retry: immediate
2. Second retry: after `retry_delay` seconds
3. Third retry: after `retry_delay * 2` seconds

After all retries exhausted, the event is logged and dropped.

## Security Considerations

1. **Use HTTPS** - Always use HTTPS endpoints in production
2. **Validate Secrets** - Verify webhook signatures
3. **Limit Access** - Firewall webhook endpoints
4. **Log Events** - Monitor webhook delivery attempts

## Troubleshooting

### Webhook Not Triggering

1. Check webhook is enabled in config
2. Verify event type is registered
3. Check manager.start() was called

### Delivery Failures

1. Verify endpoint URL is accessible
2. Check timeout configuration
3. Review logs for error details

### Signature Verification Fails

1. Ensure secret matches configuration
2. Check for timing issues (use constant-time comparison)
3. Verify payload hasn't been modified

## See Also

- [Architecture](ARCHITECTURE.md) - System architecture
- [Configuration](config.md) - Configuration options
- [TROUBLESHOOTING.md](troubleshooting.md) - Common issues
