# ChronicleMCP Architecture

This document describes the internal architecture of ChronicleMCP.

## Overview

ChronicleMCP is a secure, local-first Model Context Protocol (MCP) server that provides AI agents with access to local browser history data.

```
┌─────────────────────────────────────────────────────────────┐
│                      ChronicleMCP                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │   CLI       │    │   MCP       │    │   HTTP      │   │
│  │   Interface │    │   Server    │    │   Server    │   │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘   │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                             │                               │
│                    ┌────────▼────────┐                     │
│                    │   Connection    │                     │
│                    │   Manager       │                     │
│                    └────────┬────────┘                     │
│                             │                               │
│                    ┌────────▼────────┐                     │
│                    │   Database     │                     │
│                    │   Operations   │                     │
│                    └────────┬────────┘                     │
│                             │                               │
│                    ┌────────▼────────┐                     │
│                    │   Browser      │                     │
│                    │   Paths         │                     │
│                    └─────────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
chronicle-mcp/
├── server.py                 # MCP server with tools
├── chronicle_mcp/
│   ├── __init__.py          # Package exports
│   ├── cli.py               # CLI commands
│   ├── connection.py        # Database connection management
│   ├── config.py            # Configuration loading
│   ├── database.py          # Query functions
│   ├── paths.py             # Browser path detection
│   └── server_http.py       # HTTP server
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_*.py            # All tests
├── Dockerfile               # Container definition
├── pyproject.toml          # Project configuration
└── README.md               # Documentation
```

## Components

### 1. CLI Interface (`chronicle_mcp/cli.py`)

The CLI provides command-line access to ChronicleMCP functionality.

**Commands:**
- `run` - Run MCP server (stdio or SSE)
- `serve` - Start long-running HTTP server
- `status` - Check server status
- `logs` - View server logs
- `version` - Show version
- `list-browsers` - List available browsers
- `completion` - Generate shell completions

### 2. MCP Server (`server.py`)

The MCP (Model Context Protocol) server provides tools for AI agents.

**Available Tools:**
- `search_history` - Search by query
- `get_recent_history` - Recent history
- `count_visits` - Count domain visits
- `list_top_domains` - Top domains
- `search_history_by_date` - Date-range search
- `list_available_browsers` - List browsers

### 3. HTTP Server (`chronicle_mcp/server_http.py`)

Provides RESTful API endpoints for web applications.

**Endpoints:**
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /metrics` - Basic metrics
- `GET /api/browsers` - List browsers
- `POST /api/search` - Search history
- `POST /api/recent` - Recent history
- `POST /api/count` - Count visits
- `POST /api/top-domains` - Top domains
- `POST /api/search-date` - Search by date

### 4. Connection Manager (`chronicle_mcp/connection.py`)

Manages database connections with safety features:

- **Temp File Copying**: Creates temporary copies of browser databases to avoid "Database Locked" errors
- **Auto Cleanup**: Removes temp files after each query
- **Error Handling**: Specific error types for different failure modes:
  - `BrowserNotFoundError`
  - `BrowserPathNotFoundError`
  - `PermissionError`
  - `DatabaseLockedError`

### 5. Database Operations (`chronicle_mcp/database.py`)

Core database query functions:

- `query_history()` - Search history
- `query_recent_history()` - Recent entries
- `count_domain_visits()` - Count visits
- `get_top_domains()` - Top domains
- `search_by_date()` - Date-range search
- `format_results()` - Format output
- `sanitize_url()` - Remove sensitive params
- `format_chrome_timestamp()` - Convert timestamps

### 6. Browser Paths (`chronicle_mcp/paths.py`)

Detects browser history database paths:

**Supported Browsers:**
- Chrome (Windows, macOS, Linux)
- Edge (Windows, macOS, Linux)
- Firefox (Windows, macOS, Linux)

## Data Flow

### Query Flow

```
1. CLI/MCP/HTTP receives request
         ↓
2. Validate input parameters
         ↓
3. Get browser path from paths.py
         ↓
4. Create temp database copy (connection.py)
         ↓
5. Execute query (database.py)
         ↓
6. Format results
         ↓
7. Clean up temp file
         ↓
8. Return response
```

### Temp File Lifecycle

```
Query Request
     ↓
Create temp filename (unique per query)
     ↓
Copy browser DB to temp file
     ↓
Open SQLite connection
     ↓
Execute query
     ↓
Close connection
     ↓
Delete temp file
     ↓
Response
```

## Security

### Privacy-First Design

1. **Local Only**: All data stays on the local machine
2. **No Cloud Sync**: No external servers contacted
3. **Temp Files**: Browser DB copied to temp location
4. **Auto Cleanup**: Temp files deleted after each query

### URL Sanitization

Sensitive query parameters are automatically removed:

```python
SENSITIVE_PARAMS = {"token", "session", "key", "password", "auth", "sid", "access_token"}
```

Example:
- Input: `https://api.example.com?key=secret123&name=test`
- Output: `https://api.example.com?name=test`

### Error Messages

No sensitive information exposed in error messages:
- ✅ "Error: chrome history not found"
- ❌ "Error: /Users/john/Library/Application Support/Google/Chrome/History not found"

## Performance

### Optimization Strategies

1. **Temp File Copy**: Small files (~MB) copy quickly
2. **SQLite Indexes**: Pre-indexed columns for fast queries
3. **Limit Parameters**: Default limits prevent large result sets
4. **Connection Pooling**: Not used (each query uses fresh connection)

### Benchmarks

| Operation | Typical Time |
|-----------|--------------|
| Search (10 results) | < 100ms |
| Recent history (20 results) | < 100ms |
| Count visits | < 50ms |
| Top domains | < 100ms |
| Date-range search | < 100ms |

## Configuration

### Environment Variables

```bash
CHRONICLE_CONFIG=~/.config/chronicle-mcp/config.toml
CHRONICLE_PORT=8080
CHRONICLE_HOST=127.0.0.1
CHRONICLE_BROWSER=chrome
```

### Config File (`~/.config/chronicle-mcp/config.toml`)

```toml
[default]
browser = "chrome"
limit = 10
format = "markdown"
log_level = "INFO"
```

## Dependencies

### Core Dependencies

```
fastmcp>=0.2.0      # MCP server framework
click>=8.0.0        # CLI framework
starlette>=0.35.0   # HTTP framework
uvicorn>=0.25.0     # ASGI server
httpx>=0.25.0       # HTTP client
```

### Development Dependencies

```
pytest>=7.0.0       # Testing
pytest-cov>=4.0.0   # Coverage
ruff>=0.1.0        # Linting/formatting
mypy>=1.0.0        # Type checking
pre-commit>=3.0.0  # Git hooks
```

---

## See Also

- [CLI Reference](CLI.md)
- [API Documentation](API.md)
- [Installation Guide](INSTALL.md)
- [GitHub Repository](https://github.com/nikolasil/chronicle-mcp)
