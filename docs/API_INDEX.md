# ChronicleMCP HTTP API Overview

This section provides documentation for the ChronicleMCP HTTP API.

## Documents

- [API Reference](api.md) - Complete HTTP API reference
- [Endpoints Reference](api_endpoints.md) - Complete endpoint reference (detailed parameter tables)
- [API Examples](api_examples.md) - cURL examples and usage patterns

## Base URL

```
http://localhost:8080
```

All endpoints are relative to this base URL.

---

## Quick Start

### Health Check

```bash
curl http://localhost:8080/health
```

### List Browsers

```bash
curl http://localhost:8080/api/browsers
```

### Search History

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python tutorial", "limit": 10}'
```

---

## Output Formats

All endpoints support two output formats:

| Format | Usage | Description |
|--------|-------|-------------|
| `markdown` | Default | Human-readable formatted text |
| `json` | Add `"format": "json"` | Structured JSON data |

---

## Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `browser` | String | `chrome` | Browser to query |
| `limit` | Integer | Varies | Maximum number of results |
| `format` | String | `markdown` | Output format |

---

## Error Responses

| HTTP Status | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Browser/history not found |
| 500 | Internal Error - Server error |

---

## See Also

- [CLI Reference](cli.md)
- [Installation Guide](install.md)
- [Architecture](architecture.md)