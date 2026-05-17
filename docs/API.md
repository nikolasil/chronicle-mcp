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
  "version": "1.4.0",
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
  "browsers": ["chrome", "edge", "firefox", "brave", "vivaldi", "opera"],
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
  "browsers": ["chrome", "edge", "firefox", "brave", "safari", "vivaldi", "opera"]
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

### Delete History

**POST** `/api/delete`

Delete history entries matching a query.

**Request Body:**

```json
{
  "query": "spam.com",
  "limit": 100,
  "browser": "chrome",
  "confirm": false
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | Yes | - | Search term to match for deletion |
| `limit` | Integer | No | 100 | Maximum entries to delete (1-500) |
| `browser` | String | No | chrome | Browser to delete from |
| `confirm` | Boolean | No | false | If false, returns preview only |

**Response (200 OK - Preview):**

```json
{
  "preview": true,
  "query": "spam.com",
  "count": 5,
  "message": "Would delete 5 entries. Set confirm=true to actually delete."
}
```

**Response (200 OK - Deleted):**

```json
{
  "deleted": 5,
  "query": "spam.com",
  "browser": "chrome",
  "message": "Successfully deleted 5 entries"
}
```

---

### Search by Domain

**POST** `/api/domain-search`

Search history within specific domain(s).

**Request Body:**

```json
{
  "domain": "github.com",
  "query": "issues",
  "limit": 20,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `domain` | String | Yes | - | Domain to search within |
| `query` | String | No | - | Optional search term within domain |
| `limit` | Integer | No | 20 | Maximum results (1-100) |
| `browser` | String | No | chrome | Browser to search |
| `format` | String | No | markdown | Output format (markdown/json) |
| `exclude_domains` | Array | No | - | Domains to exclude |

**Response (200 OK):**

```json
{
  "domain": "github.com",
  "results": [
    {"title": "Issue #123", "url": "https://github.com/user/repo/issues/123", "timestamp": "2024-01-15T10:30:00+00:00"}
  ],
  "count": 1
}
```

---

### Browser Statistics

**POST** `/api/stats`

Get browsing statistics for the browser database.

**Request Body:**

```json
{
  "browser": "chrome"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `browser` | String | No | chrome | Browser to get stats for |

**Response (200 OK):**

```json
{
  "total_visits": 15000,
  "unique_domains": 500,
  "total_urls": 8000,
  "date_range": {
    "oldest": "2023-01-01T00:00:00+00:00",
    "newest": "2024-01-15T10:30:00+00:00"
  },
  "browser": "chrome"
}
```

---

### Most Visited Pages

**POST** `/api/most-visited`

Get the most visited individual pages.

**Request Body:**

```json
{
  "limit": 20,
  "browser": "chrome"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | Integer | No | 20 | Maximum pages (1-100) |
| `browser` | String | No | chrome | Browser to query |

**Response (200 OK):**

```json
{
  "pages": [
    {"title": "Home", "url": "https://example.com/", "visits": 150},
    {"title": "About", "url": "https://example.com/about", "visits": 75}
  ]
}
```

---

### Export History

**POST** `/api/export`

Export history to CSV or JSON format.

**Request Body:**

```json
{
  "format_type": "csv",
  "limit": 1000,
  "query": "python",
  "browser": "chrome"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `format_type` | String | No | csv | Export format (csv/json) |
| `limit` | Integer | No | 1000 | Maximum entries (1-10000) |
| `query` | String | No | - | Optional search filter |
| `browser` | String | No | chrome | Browser to export from |

**Response (200 OK):**

Returns raw CSV or JSON content with appropriate Content-Type header.

---

### Advanced Search

**POST** `/api/advanced-search`

Advanced search with multiple options.

**Request Body:**

```json
{
  "query": "python",
  "limit": 20,
  "browser": "chrome",
  "format": "markdown",
  "exclude_domains": ["ads.example.com"],
  "sort_by": "date",
  "use_regex": false,
  "use_fuzzy": false,
  "fuzzy_threshold": 0.6
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | Yes | - | Search term |
| `limit` | Integer | No | 20 | Maximum results |
| `browser` | String | No | chrome | Browser to search |
| `format` | String | No | markdown | Output format |
| `exclude_domains` | Array | No | - | Domains to exclude |
| `sort_by` | String | No | date | Sort order (date/visit_count/title) |
| `use_regex` | Boolean | No | false | Use regex matching |
| `use_fuzzy` | Boolean | No | false | Use fuzzy matching |
| `fuzzy_threshold` | Float | No | 0.6 | Min similarity (0.0-1.0) |

**Response (200 OK):**

```json
{
  "query": "python",
  "results": [...],
  "count": 10,
  "options": {
    "sort_by": "date",
    "use_regex": false,
    "use_fuzzy": false
  }
}
```

---

### Sync History

**POST** `/api/sync`

Sync history between browsers.

**Request Body:**

```json
{
  "source_browser": "chrome",
  "target_browser": "firefox",
  "merge_strategy": "latest",
  "dry_run": true
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `source_browser` | String | Yes | - | Browser to copy from |
| `target_browser` | String | Yes | - | Browser to copy to |
| `merge_strategy` | String | No | latest | How to handle duplicates (latest/combine/dedupe) |
| `dry_run` | Boolean | No | true | If true, show preview only |

**Response (200 OK):**

```json
{
  "dry_run": false,
  "source": "chrome",
  "target": "firefox",
  "entries_count": 150,
  "merge_strategy": "latest",
  "message": "Successfully synced 150 entries from chrome to firefox"
}
```

---

### Prometheus Metrics

**GET** `/metrics/prometheus`

Get metrics in Prometheus format.

**Response (200 OK):**

```
# HELP chronicle_uptime_seconds Server uptime in seconds
# TYPE chronicle_uptime_seconds gauge
chronicle_uptime_seconds 3600

# HELP chronicle_requests_total Total number of requests
# TYPE chronicle_requests_total counter
chronicle_requests_total 1500
...
```

---

### List Bookmarks

**GET** `/api/bookmarks`

Get list of browsers with available bookmarks.

**Response (200 OK):**

```json
{
  "browsers": ["chrome", "edge", "firefox"]
}
```

---

### Query Bookmarks

**POST** `/api/bookmarks/query`

Query bookmarks from a browser.

**Request Body:**

```json
{
  "query": "python",
  "limit": 50,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | No | - | Search term |
| `limit` | Integer | No | 50 | Maximum results |
| `browser` | String | No | chrome | Browser to query |
| `format` | String | No | markdown | Output format |

**Response (200 OK):**

```json
{
  "results": [
    {
      "title": "Python Tutorial",
      "url": "https://docs.python.org/",
      "timestamp": "2024-01-15T10:30:00+00:00"
    }
  ],
  "count": 1
}
```

---

### List Downloads

**GET** `/api/downloads`

Get list of browsers with available downloads history.

**Response (200 OK):**

```json
{
  "browsers": ["chrome", "edge", "firefox"]
}
```

---

### Query Downloads

**POST** `/api/downloads/query`

Query downloads history from a browser.

**Request Body:**

```json
{
  "query": "pdf",
  "limit": 50,
  "browser": "chrome",
  "format": "markdown"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | String | No | - | Search term |
| `limit` | Integer | No | 50 | Maximum results |
| `browser` | String | No | chrome | Browser to query |
| `format` | String | No | markdown | Output format |

**Response (200 OK):**

```json
{
  "results": [
    {
      "title": "document.pdf",
      "url": "https://example.com/document.pdf",
      "timestamp": "2024-01-15T10:30:00+00:00",
      "state": "COMPLETE",
      "total_bytes": 1024000
    }
  ],
  "count": 1
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
| 1.4.0 | 2024-03-15 | Advanced analytics, productivity analysis |
| 1.3.0 | 2024-02-20 | Bookmarks and downloads |
| 1.2.0 | 2024-01-10 | Cross-browser sync |
| 1.1.0 | 2023-12-05 | Multi-browser support |
| 1.0.0 | 2023-11-01 | Initial release |

---

## See Also

- [CLI Reference](cli.md)
- [Installation Guide](install.md)
- [Architecture](architecture.md)
