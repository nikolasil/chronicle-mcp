# Real-time Subscriptions Guide

ChronicleMCP supports real-time subscriptions to browser history changes. This enables applications to receive notifications when history entries are added, deleted, or modified.

## Overview

The subscription system uses a publish/subscribe model where you:
1. Subscribe to specific event types for a browser
2. Receive notifications when matching events occur
3. Unsubscribe when you no longer need the notifications

## Available Event Types

| Event Type | Description |
|------------|-------------|
| `history_added` | New history entry was added |
| `history_deleted` | History entry was deleted |
| `history_updated` | History entry was modified |
| `bookmark_added` | New bookmark was added |
| `bookmark_deleted` | Bookmark was deleted |
| `download_added` | New download entry was added |
| `download_deleted` | Download entry was deleted |

## MCP Tools

### Subscribe to History Changes

```python
result = subscribe_to_history(
    browser="chrome",
    event_types=["history_added", "history_deleted"]
)
```

**Response:**
```json
{
  "subscription_id": "550e8400-e29b-41d4-a716-446655440000",
  "browser": "chrome",
  "event_types": ["history_added", "history_deleted"],
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Unsubscribe

```python
result = unsubscribe_from_history(subscription_id="550e8400-e29b-41d4-a716-446655440000")
```

**Response:**
```json
{
  "success": true,
  "subscription_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Get Subscription Status

```python
# Get specific subscription
result = get_subscription_status(subscription_id="550e8400-e29b-41d4-a716-446655440000")

# Get global statistics (no subscription_id)
result = get_subscription_status()
```

**Response (specific):**
```json
{
  "subscription_id": "550e8400-e29b-41d4-a716-446655440000",
  "browser": "chrome",
  "event_types": ["history_added", "history_deleted"],
  "status": "active",
  "events_received": 42,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Response (global stats):**
```json
{
  "total_subscriptions": 3,
  "total_events": 156,
  "events_by_type": {
    "history_added": 120,
    "history_deleted": 36
  },
  "events_by_browser": {
    "chrome": 100,
    "firefox": 56
  },
  "last_event_time": "2024-01-15T14:22:00Z"
}
```

## Architecture

### SubscriptionManager

The `SubscriptionManager` class (in `chronicle_mcp/core/realtime.py`) handles:
- Creating and tracking subscriptions
- Publishing events to matching subscriptions
- Managing subscription lifecycle
- Collecting event statistics

### EventBroadcaster

The `EventBroadcaster` class provides async support for SSE/WebSocket streaming:
- Async connection management
- Queue-based event delivery
- Connection health monitoring

## Use Cases

### 1. Activity Monitor

Monitor browsing activity in real-time:
```python
subscribe_to_history(
    browser="chrome",
    event_types=["history_added"]
)
```

### 2. Sync Notification

Trigger actions when history changes:
```python
subscribe_to_history(
    browser="chrome", 
    event_types=["history_added", "history_deleted"]
)
```

### 3. Bookmark Backup

Monitor bookmark changes:
```python
subscribe_to_history(
    browser="chrome",
    event_types=["bookmark_added", "bookmark_deleted"]
)
```

## HTTP API

### Subscribe (HTTP)

```
POST /api/subscribe
Content-Type: application/json

{
  "browser": "chrome",
  "event_types": ["history_added", "history_deleted"]
}
```

### Unsubscribe (HTTP)

```
DELETE /api/subscribe/{subscription_id}
```

### Get Status (HTTP)

```
GET /api/subscribe/{subscription_id}
```

### Global Stats (HTTP)

```
GET /api/subscriptions/stats
```

## Event Payload Format

Events delivered to callbacks have this structure:

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

## Limitations

1. **Callback Required:** The MCP tool `subscribe_to_history` requires a callback function for event delivery. In stdio mode, callbacks are executed but output isn't streamed back to the client in real-time.

2. **No Persistent Subscriptions:** Subscriptions are in-memory and don't persist across server restarts.

3. **Rate Limiting:** High-frequency events may be queued but not dropped.

4. **Browser Scope:** Each subscription is tied to a single browser.

## Future Enhancements

Planned improvements:
- WebSocket support for real-time streaming
- Persistent subscriptions (database-backed)
- Event replay capability
- Subscription groups/multicast
- TLS/SSL for SSE transport

## Security Notes

- Event delivery happens locally via callbacks
- No network exposure in stdio mode
- SSE mode requires network configuration
- Sensitive URL parameters are sanitized in events

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [ANALYTICS.md](ANALYTICS.md) - Analytics features
- [API.md](API.md) - HTTP API reference