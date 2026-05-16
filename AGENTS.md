# AGENTS.md - ChronicleMCP Development Guide

## Project Overview

ChronicleMCP is a Python-based Model Context Protocol (MCP) server that provides AI agents secure access to local browser history. The project uses a layered architecture with the FastMCP framework and SQLite for fast, privacy-first local data access.

**Main Entry Point:** `chronicle_mcp/server.py`
**CLI Entry Point:** `chronicle_mcp/cli.py`
**MCP Protocol:** `chronicle_mcp/protocols/mcp.py`
**HTTP Protocol:** `chronicle_mcp/protocols/http.py`
**Core Service:** `chronicle_mcp/core/services.py`
**Connection Management:** `chronicle_mcp/connection.py`

---

## Build, Lint, and Test Commands

### Installation

```bash
pip install -e ".[dev]"
```

### Development Server

```bash
# MCP server (stdio mode - for AI assistants)
chronicle-mcp mcp

# MCP server (SSE mode)
chronicle-mcp mcp --sse --host 127.0.0.1 --port 8080

# HTTP REST API server
chronicle-mcp http --port 8080
```

### Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Run with verbose output
pytest tests/            # Run specific test directory
pytest tests/unit/core/test_validation.py  # Run specific test file
pytest -k test_name      # Run single test by name
pytest --co             # List all tests without running
pytest --cov=chronicle_mcp  # With coverage
```

### Linting

```bash
ruff check .                 # Check linting
ruff check . --fix          # Auto-fix issues
ruff format .               # Format code
ruff format . --check      # Check formatting
```

### Type Checking

```bash
mypy chronicle_mcp/        # Type checking
```

---

## CLI Commands

### Available Commands

```bash
# Run MCP server (for AI assistants)
chronicle-mcp mcp                          # stdio mode (default)
chronicle-mcp mcp --sse                   # SSE mode

# Run HTTP REST API server
chronicle-mcp http --port 8080            # Foreground
chronicle-mcp http --port 8080 --daemon   # Background

# Check HTTP server status
chronicle-mcp status --port 8080

# View HTTP server logs
chronicle-mcp logs --port 8080 --lines 50

# Check version
chronicle-mcp version

# List browsers
chronicle-mcp list-browsers

# Generate completions
chronicle-mcp completion bash >> ~/.bashrc
```

---

## Architecture Overview

### Layered Architecture

```
Protocol Layer (protocols/)
├── mcp.py          # MCP protocol adapter
└── http.py         # HTTP protocol adapter

Service Layer (core/)
├── services.py     # HistoryService - all business logic
├── validation.py   # Input validation
├── formatters.py   # Response formatting
└── exceptions.py   # Service exceptions

Infrastructure Layer
├── connection.py   # Database connections
├── database.py     # Query operations
├── paths.py        # Browser path detection
└── config.py       # Configuration
```

### Key Principle

**All business logic lives in the Service Layer.** Protocol adapters are thin wrappers that:
1. Receive protocol-specific requests
2. Call `HistoryService` methods
3. Convert results to protocol-specific responses
4. Handle service exceptions appropriately

---

## Code Style Guidelines

### Imports

Group imports: standard library → third-party → local application

```python
import logging
from typing import Any

from fastmcp import FastMCP

from chronicle_mcp.core import HistoryService, validate_browser
from chronicle_mcp.connection import get_history_connection
```

### Service Layer Pattern

```python
from chronicle_mcp.core import HistoryService

# In protocol adapter:
result = HistoryService.search_history(
    query="python",
    limit=10,
    browser="chrome",
    format_type="markdown"
)
# result is a dict with "results", "count", "message", etc.
```

### Error Handling in Protocols

```python
from chronicle_mcp.core import ServiceError

try:
    result = HistoryService.search_history(...)
    return result["message"]
except ServiceError as e:
    # For MCP:
    return f"Error: {e.message}"
    # For HTTP:
    return JSONResponse({"error": e.message}, status_code=400)
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `get_history_path` |
| Variables | snake_case | `history_path` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_LIMIT` |
| Classes | PascalCase | `HistoryService` |
| Exceptions | PascalCase | `ValidationError` |

---

## MCP Tool Functions

All MCP tools delegate to `HistoryService` methods. Here's the complete list of available tools:

### 1. Browser Management

#### `list_available_browsers()`

Returns a list of browsers with detected history databases on this system.

#### `list_available_bookmarks()`

Returns a list of browsers with detected bookmarks on this system.

#### `list_available_downloads()`

Returns a list of browsers with detected downloads history on this system.

---

### 2. Basic Search Operations

#### `search_history(query, limit, browser, format_type)`

Search browser history for keywords in titles or URLs.

```python
result = HistoryService.search_history(
    query="python",
    limit=10,
    browser="chrome",
    format_type="markdown"
)
return result["message"]
```

#### `get_recent_history(hours, limit, browser, format_type)`

Gets recent browsing history from the last N hours.

#### `count_visits(domain, browser)`

Counts total visits to a specific domain.

#### `list_top_domains(limit, browser, format_type)`

Gets the most visited domains from browser history.

#### `get_most_visited_pages(limit, browser, format_type)`

Gets the most visited individual pages.

---

### 3. Advanced Search Operations

#### `search_history_by_date(query, start_date, end_date, limit, browser, format_type)`

Searches browser history within a date range.

#### `search_by_domain(domain, query, limit, browser, format_type, exclude_domains)`

Searches history within specific domain(s).

#### `search_history_advanced(query, limit, browser, format_type, exclude_domains, sort_by, use_regex, use_fuzzy, fuzzy_threshold)`

Advanced search with multiple options.

#### `get_browser_stats(browser)`

Gets browsing statistics for the browser database.

---

### 4. History Management

#### `delete_history(query, limit, browser, confirm)`

Deletes history entries matching a query.

#### `sync_history(source_browser, target_browser, merge_strategy, dry_run)`

Syncs history between browsers.

#### `export_history(format_type, limit, query, browser)`

Exports history to CSV or JSON format.

---

### 5. Bookmarks and Downloads

#### `get_bookmarks(query, limit, browser, format_type)`

Gets bookmarks from a browser.

#### `get_downloads(query, limit, browser, format_type)`

Gets downloads history from a browser.

---

## Testing

### Unit Tests Structure

```
tests/
├── unit/
│   ├── core/           # Service layer tests
│   │   ├── test_validation.py
│   │   ├── test_formatters.py
│   │   ├── test_services.py
│   │   ├── test_analytics.py
│   │   ├── test_categories.py
│   │   └── test_exceptions.py
│   ├── protocols/      # Protocol adapter tests
│   │   ├── test_mcp.py
│   │   └── test_http.py
│   └── infrastructure/ # Infrastructure tests
│       ├── test_database.py
│       ├── test_connection.py
│       ├── test_paths.py
│       ├── test_cli.py
│       ├── test_cache.py
│       ├── test_webhooks.py
│       └── test_config.py
├── integration/        # Integration tests
│   └── test_browser.py
└── benchmark/          # Performance tests
    └── test_performance.py
```

### Test Fixtures and Isolation

```
tests/conftest.py       # Shared fixtures and configuration
test_isolation.py      # Tests to verify isolation works correctly
```

**Key Fixtures:**
- `mock_chrome_path` - Mocks browser path detection
- `sample_chrome_db` - Creates sample Chrome database
- `realistic_chrome_db` - Creates session-scoped DB with realistic timestamps
- `temp_dir` / `tmp_path` - Isolated temporary directories
- `http_client` - HTTP client with fresh app per test
- `cleanup_default_cache` - Session-scoped cache teardown (autouse)
- `cleanup_webhook_manager` - Session-scoped webhook teardown (autouse)

### Writing Tests

```python
# tests/unit/core/test_validation.py
import pytest
from chronicle_mcp.core import validate_browser, ValidationError

def test_valid_browser():
    result = validate_browser("chrome")
    assert result == "chrome"

def test_invalid_browser():
    with pytest.raises(ValidationError):
        validate_browser("invalid")
```

---

## Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `cli.py` | Command-line interface, process management |
| `protocols/mcp.py` | MCP protocol server with tools |
| `protocols/http.py` | HTTP REST API server |
| `core/services.py` | Business logic, validation, orchestration |
| `core/validation.py` | Input validation functions |
| `core/formatters.py` | Response formatting |
| `core/exceptions.py` | Service-level exceptions |
| `connection.py` | Database connection management |
| `database.py` | Query operations |
| `paths.py` | Browser path detection |
| `config.py` | Configuration loading |

---

## See Also

- [Architecture](ARCHITECTURE.md) - Detailed architecture documentation
- [CLI Reference](CLI.md) - CLI command reference
- [API Documentation](API.md) - HTTP API reference
- [Installation Guide](INSTALL.md) - Installation instructions
