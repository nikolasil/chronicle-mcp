# ChronicleMCP HTTP API Reference

This document provides a complete reference for the ChronicleMCP HTTP API.

## Base URL

```
http://localhost:8080
```

All endpoints are relative to this base URL.

---

## Endpoints

### Health Check

**GET** `/health`

Check if the service is healthy.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "service": "chronicle-mcp",
  "version": "1.1.0",
  "timestamp": "2024-01-15T10:30:00+00:00"
}
```

---

### Readiness Check

**GET** `/ready`

Check if the service is ready and browsers are available.

**Response (200 OK):**

```json
{
  "status": "ready",
  "service": "chronicle-mcp",
  "browsers": ["chrome", "edge"],
  "timestamp": "2024-01-15T10:30:00+00:00"
}
```

**Response (200 OK - No browsers):**

```json
{
  "status": "degraded",
  "service": "chronicle-mcp",
  "browsers": [],
  "timestamp": "2024-01-15T10:30:00+00:00"
}
```

---

### Metrics

**GET** `/metrics`

Get basic metrics about the service.

**Response (200 OK):**

```json
{
  "uptime_seconds": 3600,
  "requests_total": 1500,
  "browsers_available": 2
}
```

---

### List Browsers

**GET** `/api/browsers`

Get a list of available browsers.

**Response (200 OK):**

```json
{
  "browsers": ["chrome", "edge", "firefox"]
}
```

---

### Search History

**POST** `/api/search`

Search browser history for keywords.

**Request Body:**

```json
{
  "query": "python tutorial",
  "limit": 10,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | Yes | - | Search term |
| `limit` | Integer | No | 5 | Maximum results (1-100) |
| `browser` | String | No | chrome | Browser to search |
| `format` | String | No | markdown | Output format (markdown/json) |

**Response (200 OK):**

```json
{
  "results": [
    {
      "title": "Python Tutorial",
      "url": "https://docs.python.org/3/tutorial/",
      "timestamp": "2024-01-15T10:30:00+00:00"
    }
  ],
  "count": 1
}
```

**Response (400 Bad Request):**

```json
{
  "error": "Query cannot be empty"
}
```

**Response (404 Not Found):**

```json
{
  "error": "chrome history not found"
}
```

---

### Recent History

**POST** `/api/recent`

Get recent browsing history.

**Request Body:**

```json
{
  "hours": 24,
  "limit": 20,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `hours` | Integer | No | 24 | Hours to look back |
| `limit` | Integer | No | 20 | Maximum results (1-100) |
| `browser` | String | No | chrome | Browser to search |
| `format` | String | No | markdown | Output format (markdown/json) |

**Response (200 OK):**

```json
{
  "results": [
    {
      "title": "Recent Page",
      "url": "https://example.com/",
      "timestamp": "2024-01-15T10:30:00+00:00"
    }
  ],
  "count": 1
}
```

---

### Count Visits

**POST** `/api/count`

Count visits to a specific domain.

**Request Body:**

```json
{
  "domain": "github.com",
  "browser": "chrome"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `domain` | String | Yes | - | Domain to count |
| `browser` | String | No | chrome | Browser to search |

**Response (200 OK):**

```json
{
  "domain": "github.com",
  "browser": "chrome",
  "count": 42
}
```

**Response (400 Bad Request):**

```json
{
  "error": "Domain cannot be empty"
}
```

---

### Top Domains

**POST** `/api/top-domains`

Get the most visited domains.

**Request Body:**

```json
{
  "limit": 10,
  "browser": "chrome"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | Integer | No | 10 | Maximum domains (1-50) |
| `browser` | String | No | chrome | Browser to search |

**Response (200 OK):**

```json
{
  "domains": [
    {"domain": "github.com", "visits": 150},
    {"domain": "stackoverflow.com", "visits": 75},
    {"domain": "docs.python.org", "visits": 50}
  ]
}
```

---

### Search by Date

**POST** `/api/search-date`

Search history within a date range.

**Request Body:**

```json
{
  "query": "python",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "limit": 10,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | Yes | - | Search term |
| `start_date` | String | Yes | - | Start date (YYYY-MM-DD) |
| `end_date` | String | Yes | - | End date (YYYY-MM-DD) |
| `limit` | Integer | No | 10 | Maximum results (1-100) |
| `browser` | String | No | chrome | Browser to search |
| `format` | String | No | markdown | Output format (markdown/json) |

**Response (200 OK):**

```json
{
  "results": [
    {
      "title": "Python Documentation",
      "url": "https://docs.python.org/",
      "timestamp": "2024-01-15T10:30:00+00:00"
    }
  ],
  "count": 1
}
```

**Response (400 Bad Request):**

```json
{
  "error": "query, start_date, and end_date are required"
}
```

---

## cURL Examples

### Search History

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python tutorial", "limit": 10, "browser": "chrome"}'
```

### Get Recent History

```bash
curl -X POST http://localhost:8080/api/recent \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "limit": 20}'
```

### Count Domain Visits

```bash
curl -X POST http://localhost:8080/api/count \
  -H "Content-Type: application/json" \
  -d '{"domain": "github.com"}'
```

### Get Health Status

```bash
curl http://localhost:8080/health
```

### List Browsers

```bash
curl http://localhost:8080/api/browsers
```

---

## Rate Limiting

Currently, ChronicleMCP does not implement rate limiting. Future versions may include:

- Request rate limits per IP
- Connection limits
- Query throttling

---

## Error Codes

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | Bad Request | Invalid input parameters |
| 404 | Not Found | Browser or history not found |
| 403 | Forbidden | Permission denied |
| 500 | Internal Error | Server error |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2024-02-12 | Initial HTTP API |
| 1.0.0 | 2024-01-15 | Initial release |

---

## See Also

- [CLI Reference](CLI.md)
- [Installation Guide](INSTALL.md)
- [Architecture](ARCHITECTURE.md)
