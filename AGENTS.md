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
# MCP Inspector for stdio mode
python -m chronicle_mcp.server dev

# HTTP server for testing
chronicle-mcp serve --port 8080
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
# Run MCP server
chronicle-mcp run                          # stdio mode
chronicle-mcp run --transport sse        # SSE mode

# Start HTTP server
chronicle-mcp serve --port 8080          # Foreground
chronicle-mcp serve --port 8080 --daemon  # Background

# Check status
chronicle-mcp status --port 8080

# View logs
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

```python
@mcp.tool()
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
    """
    Searches browser history for keywords in titles or URLs.

    Args:
        query: Search term to look for
        limit: Maximum number of results (1-100)
        browser: Browser to search
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of matching history entries
    """
    # Delegate to service layer
    result = HistoryService.search_history(...)
    return result["message"]
```

---

## Testing

### Unit Tests Structure

```
tests/
├── unit/
│   ├── core/           # Service layer tests
│   │   ├── test_validation.py
│   │   ├── test_formatters.py
│   │   └── test_services.py
│   ├── protocols/      # Protocol adapter tests
│   │   ├── test_mcp.py
│   │   └── test_http.py
│   └── infrastructure/ # Infrastructure tests
│       ├── test_database.py
│       ├── test_connection.py
│       └── test_paths.py
└── integration/        # Integration tests
```

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

## Migration from Old Structure

### Old imports:
```python
from server import mcp, search_history
from chronicle_mcp.server_http import run_http_server
```

### New imports:
```python
from chronicle_mcp.protocols import mcp
from chronicle_mcp.protocols.http import run_http_server
from chronicle_mcp.core import HistoryService
```

---

## See Also

- [Architecture](ARCHITECTURE.md) - Detailed architecture documentation
- [CLI Reference](CLI.md) - CLI command reference
- [API Documentation](API.md) - HTTP API reference
- [Installation Guide](INSTALL.md) - Installation instructions
