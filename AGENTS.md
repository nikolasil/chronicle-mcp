# AGENTS.md - ChronicleMCP Development Guide

## Project Overview

ChronicleMCP is a Python-based Model Context Protocol (MCP) server that provides AI agents secure access to local browser history. The project uses the FastMCP framework and SQLite for fast, privacy-first local data access.

**Main Entry Point:** `server.py`
**CLI Entry Point:** `chronicle_mcp/cli.py`
**HTTP Server:** `chronicle_mcp/server_http.py`
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
python server.py dev

# HTTP server for testing
chronicle-mcp serve --port 8080
```

### Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Run with verbose output
pytest tests/            # Run specific test directory
pytest tests/test_database.py  # Run specific test file
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
mypy chronicle_mcp/ server.py  # Type checking
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

## Code Style Guidelines

### Imports

Group imports: standard library → third-party → local application

```python
import logging
import os
import shutil
import sqlite3
import tempfile
import time
from collections.abc import Generator
from contextlib import contextmanager

from fastmcp import FastMCP

from chronicle_mcp.config import setup_logging
from chronicle_mcp.connection import get_history_connection
from chronicle_mcp.database import query_history, format_results
from chronicle_mcp.paths import get_browser_path, get_available_browsers
```

### Formatting

- 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate logical sections
- No trailing whitespace
- Add final newline to files

### Type Hints

```python
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `get_history_path` |
| Variables | snake_case | `history_path` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_LIMIT` |
| Private functions | prefix with underscore | `_internal_helper` |
| Classes | PascalCase | `ConnectionError` |
| Exceptions | PascalCase | `BrowserNotFoundError` |

### Docstrings

```python
def get_history_connection(browser: str = "chrome") -> Generator[sqlite3.Connection, None, None]:
    """
    Creates a temporary copy of the history DB to avoid 'Database Locked' errors.

    Args:
        browser: Browser name (chrome, edge, firefox)

    Yields:
        SQLite connection to the history database

    Raises:
        BrowserNotFoundError: If browser is not recognized
        BrowserPathNotFoundError: If history path doesn't exist
    """
```

### Error Handling

```python
try:
    with get_history_connection(browser) as conn:
        rows = query_history(conn, query, limit)
        return format_results(rows, query, format_type)
except BrowserNotFoundError:
    return f"Error: {browser} history not found"
except PermissionError:
    return f"Error: Permission denied accessing {browser} history"
except sqlite3.OperationalError:
    return f"Error: Unable to access {browser} history database"
except Exception:
    logger.exception("Unexpected error")
    return "Error: An unexpected error occurred"
```

### MCP Tool Functions

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
```

### File Organization

```
chronicle-mcp/
├── server.py              # MCP server and tool definitions
├── chronicle_mcp/
│   ├── __init__.py       # Package exports
│   ├── cli.py            # CLI commands
│   ├── connection.py     # Database connection management
│   ├── config.py         # Configuration loading
│   ├── database.py        # Query functions and formatting
│   ├── paths.py          # Browser path detection
│   └── server_http.py     # HTTP server
└── tests/
    ├── conftest.py       # Pytest fixtures
    ├── test_*.py         # All test files
```

---

## Architecture Notes

### Component Responsibilities

| Component | Responsibility |
|-----------|-----------------|
| `cli.py` | Command-line interface |
| `server.py` | MCP protocol server with tools |
| `server_http.py` | HTTP REST API server |
| `connection.py` | Database connection management |
| `database.py` | Query operations and formatting |
| `paths.py` | Browser path detection |
| `config.py` | Configuration loading |

### Connection Flow

```
Query Request
    ↓
Validate parameters
    ↓
get_history_connection(browser)
    ↓
Copy DB to temp file
    ↓
Execute query
    ↓
Format results
    ↓
Cleanup temp file
    ↓
Return response
```

### Data Types

```python
# Connection exceptions
ConnectionError
├── BrowserNotFoundError
├── BrowserPathNotFoundError
├── PermissionError
└── DatabaseLockedError
```

---

## Testing Guidelines

### Test Fixtures

```python
@pytest.fixture
def sample_chrome_db(temp_dir):
    """Creates a synthetic Chrome history database."""
    ...

@pytest.fixture
def realistic_chrome_db(temp_dir):
    """Creates a realistic Chrome history database with 100+ entries."""
    ...
```

### Mocking Browser Paths

```python
@pytest.fixture
def mock_chrome_path(monkeypatch, sample_chrome_db):
    """Mocks get_browser_path for testing."""
    from chronicle_mcp import paths

    def mock_fn(browser):
        if browser.lower() == "chrome":
            return sample_chrome_db
        return None

    monkeypatch.setattr(paths, "get_browser_path", mock_fn)
```

### HTTP Endpoint Testing

```python
from starlette.testclient import TestClient
from chronicle_mcp.server_http import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
```

### Test Coverage Requirements

- Minimum 85% coverage
- Test all MCP tools
- Test error handling paths
- Test HTTP endpoints
- Test security features (URL sanitization)
- Test performance with large datasets

---

## Tool Naming Conflicts

When adding new tools, avoid naming conflicts:

```python
# Bad - conflicts with database.py
from chronicle_mcp.database import get_top_domains
def get_top_domains(...):  # Name conflict!

# Good - use alias
from chronicle_mcp.database import get_top_domains as db_get_top_domains
def list_top_domains(...):  # Different name
```

---

## Development Workflow

### Quick Start

```bash
# 1. Clone and install
git clone https://github.com/nikolasil/chronicle-mcp.git
cd chronicle-mcp
pip install -e ".[dev]"

# 2. Run tests
pytest -v

# 3. Run linting
ruff check . --fix
ruff format .

# 4. Start dev server
python server.py dev

# 5. Start HTTP server (separate terminal)
chronicle-mcp serve --port 8080
```

### Making Changes

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes following style guidelines
3. Add tests for new functionality
4. Run full test suite: `pytest -v`
5. Run linting: `ruff check . --fix`
6. Commit with conventional commits: `git commit -m "feat: add new tool"`
7. Push and create PR

---

## See Also

- [CLI Reference](CLI.md)
- [API Documentation](API.md)
- [Installation Guide](INSTALL.md)
- [Architecture](ARCHITECTURE.md)
