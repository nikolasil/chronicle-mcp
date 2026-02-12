# ChronicleMCP User Guide

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [MCP Tools Overview](#mcp-tools-overview)
5. [HTTP API](#http-api)
6. [Configuration](#configuration)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# Install ChronicleMCP
pip install chronicle-mcp

# Run in stdio mode (for AI agents)
chronicle-mcp run

# Or start an HTTP server
chronicle-mcp serve --port 8080

# Check available browsers
chronicle-mcp list-browsers
```

---

## Installation

### pip (Recommended)

```bash
pip install chronicle-mcp
```

### pipx (Isolated Installation)

```bash
pipx install chronicle-mcp
```

### Docker

```bash
docker pull ghcr.io/nikolasil/chronicle-mcp:latest
docker run -p 8080:8080 ghcr.io/nikolasil/chronicle-mcp
```

### From Source

```bash
git clone https://github.com/nikolasil/chronicle-mcp.git
cd chronicle-mcp
pip install -e .
```

---

## Basic Usage

### Search Your History

```python
# Search for Python tutorials
search_history("python tutorial", limit=10)

# Get recent browsing history
get_recent_history(hours=24, limit=20)

# Find pages from a specific domain
search_by_domain("github.com", query="python")

# List most visited pages
list_top_domains(limit=10)
```

### Export Your Data

```python
# Export to CSV
export_history(format_type="csv", limit=1000)

# Export to JSON
export_history(format_type="json", limit=1000)
```

### Browser Statistics

```python
# Get browsing statistics
get_browser_stats()
```

---

## MCP Tools Overview

### search_history

Search browser history for keywords.

```python
search_history(
    query: str,              # Search term
    limit: int = 5,          # Maximum results (1-100)
    browser: str = "chrome", # Browser to search
    format_type: str = "markdown"  # Output format
)
```

### get_recent_history

Get recent browsing history.

```python
get_recent_history(
    hours: int = 24,        # Look back period
    limit: int = 20,         # Maximum results
    browser: str = "chrome",
    format_type: str = "markdown"
)
```

### search_by_domain

Search within specific domain(s).

```python
search_by_domain(
    domain: str,             # Domain to search
    query: str = None,       # Optional search term
    limit: int = 20,
    browser: str = "chrome",
    exclude_domains: list[str] = None  # Domains to exclude
)
```

### delete_history

Delete history entries matching a query.

```python
delete_history(
    query: str,
    limit: int = 100,
    browser: str = "chrome",
    confirm: bool = False    # Must be True to actually delete
)
```

### search_history_advanced

Advanced search with multiple options.

```python
search_history_advanced(
    query: str,
    limit: int = 20,
    browser: str = "chrome",
    exclude_domains: list[str] = None,
    sort_by: str = "date",   # date, visit_count, title
    use_regex: bool = False,
    use_fuzzy: bool = False,
    fuzzy_threshold: float = 0.6
)
```

### get_browser_stats

Get browsing statistics.

```python
get_browser_stats(browser: str = "chrome")
```

### get_most_visited_pages

Get most visited individual pages.

```python
get_most_visited_pages(
    limit: int = 20,
    browser: str = "chrome"
)
```

### export_history

Export history to CSV or JSON.

```python
export_history(
    format_type: str = "csv",
    limit: int = 1000,
    query: str = None,
    browser: str = "chrome"
)
```

### sync_history

Sync history between browsers.

```python
sync_history(
    source_browser: str,
    target_browser: str,
    merge_strategy: str = "latest",  # latest, combine, dedupe
    dry_run: bool = True
)
```

---

## HTTP API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| GET | `/api/browsers` | List available browsers |
| POST | `/api/search` | Search history |
| POST | `/api/recent` | Recent history |
| POST | `/api/export` | Export history |
| POST | `/api/stats` | Browser statistics |

### Example Requests

```bash
# Search history
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "limit": 10}'

# Get recent history
curl -X POST http://localhost:8080/api/recent \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "limit": 20}'

# Export to JSON
curl -X POST http://localhost:8080/api/export \
  -H "Content-Type: application/json" \
  -d '{"format": "json", "limit": 1000}'
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHRONICLE_PORT` | Default port | `8080` |
| `CHRONICLE_HOST` | Default host | `127.0.0.1` |
| `CHRONICLE_BROWSER` | Default browser | `chrome` |
| `CHRONICLE_LOG_LEVEL` | Log level | `INFO` |
| `CHRONICLE_CACHE_TTL` | Cache TTL in seconds | `300` |

### Config File

Create `~/.config/chronicle-mcp/config.toml`:

```toml
[default]
browser = "chrome"
limit = 10
format = "markdown"
log_level = "INFO"

[cache]
enabled = true
ttl_seconds = 300
max_entries = 1000

[security]
sanitize_urls = true
```

---

## Troubleshooting

### Browser not found

```bash
# List available browsers
chronicle-mcp list-browsers

# Check if browser is installed
# Ensure browser is closed (locks the database)
```

### Permission denied

```bash
# Check file permissions
ls -la ~/.config/google-chrome/Default/History

# On Windows, run as administrator if needed
```

### Empty results

```bash
# Try a more specific search term
search_history("specific phrase")

# Check the date range
search_history_by_date(
    query="python",
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Performance issues

```bash
# Reduce limit parameter
search_history("query", limit=10)

# Check cache settings
# Large history databases may take longer to query
```

---

## Getting Help

- [GitHub Issues](https://github.com/nikolasil/chronicle-mcp/issues)
- [Contributing Guide](CONTRIBUTING.md)
- [API Documentation](API.md)
