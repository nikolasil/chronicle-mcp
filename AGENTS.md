# AGENTS.md - ChronicleMCP Development Guide

## Project Overview

ChronicleMCP is a Python-based Model Context Protocol (MCP) server that provides AI agents secure access to local browser history. The project uses the FastMCP framework and SQLite for fast, privacy-first local data access.

**Main Entry Point:** `server.py`
**Dependencies:** `requirements.txt` (fastmcp only)

---

## Build, Lint, and Test Commands

### Installation
```bash
pip install fastmcp
```

### Development Server
```bash
python server.py dev
```
Launches the MCP Inspector web interface for testing tools manually.

### Running Tests
```bash
pytest                    # Run all tests
pytest -v                 # Run with verbose output
pytest tests/            # Run specific test directory
pytest tests/test_database.py  # Run specific test file
pytest -k test_name      # Run single test by name
pytest --co             # List all tests without running
```

### Linting
```bash
flake8 .                 # Basic linting
flake8 --max-line-length=100 .  # Custom line length
```

### Type Checking
```bash
mypy .                   # Type checking
```

### Code Formatting
```bash
black .                  # Format all Python files
```

---

## Code Style Guidelines

### Imports
- Group imports: standard library → third-party → local application
- Use absolute imports
- Keep imports sorted alphabetically within groups
```python
import os
import sqlite3
import shutil
import tempfile
import platform
import time
from contextlib import contextmanager
from fastmcp import FastMCP
from chronicle_mcp.paths import get_browser_path, get_available_browsers
from chronicle_mcp.database import query_history, format_results
```

### Formatting
- 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use blank lines to separate logical sections (2 blank lines between top-level definitions)
- No trailing whitespace
- Add final newline to files

### Type Hints
- Use type hints for function parameters and return values
- Include default values for optional parameters
```python
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
```

### Naming Conventions
- **Functions:** snake_case (e.g., `get_history_path`, `search_history`)
- **Variables:** snake_case (e.g., `history_path`, `temp_path`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `TEMP_CACHE_DURATION`)
- **Private functions:** prefix with underscore (e.g., `_internal_helper`)
- **Tool functions:** Use descriptive names, avoid conflicts with imported functions

### Docstrings
- Use triple double-quotes for all docstrings
- Write clear, concise descriptions
- Include Args and Returns sections for complex functions
```python
def get_history_connection(browser: str = "chrome"):
    """
    Creates a temporary copy of the history DB to avoid 'Database Locked' errors.

    Args:
        browser: Browser name (chrome, edge, firefox)

    Yields:
        SQLite connection to the history database
    """
```

### Error Handling
- Use try/except blocks with specific exception types when possible
- Return user-friendly error messages for tool functions
- Avoid exposing file paths in error messages
```python
try:
    with get_history_connection(browser) as conn:
        rows = query_history(conn, query, limit)
        return format_results(rows, query, format_type)
except FileNotFoundError:
    return f"Error: {browser} history not found"
except PermissionError:
    return f"Error: Permission denied accessing {browser} history"
except sqlite3.OperationalError:
    return f"Error: Unable to access {browser} history database"
except Exception:
    return "Error: An unexpected error occurred"
```

### MCP Tool Functions
- Decorate with `@mcp.tool()`
- Always return strings (not raw data) for AI consumption
- Include docstrings describing parameters and return format
- Handle empty results gracefully with informative messages
- Validate all input parameters before processing

### File Organization
```
chronicle-mcp/
├── server.py              # MCP server and tool definitions
├── chronicle_mcp/
│   ├── __init__.py       # Package exports
│   ├── paths.py          # Browser path detection
│   └── database.py       # Query functions and formatting
└── tests/
    ├── conftest.py       # Pytest fixtures
    ├── test_paths.py     # Path detection tests
    └── test_database.py  # Database operation tests
```

### Database Operations
- Create temporary copies of database files to avoid locking issues
- Always close connections after use (use context managers)
- Clean up temp files after queries
- Use parameterized queries to prevent SQL injection
- Sanitize URLs to remove sensitive parameters

---

## Architecture Notes

- **MCP Protocol:** All tools must be decorated with `@mcp.tool()`
- **Cross-Platform:** Support Windows, macOS, and Linux via `platform.system()`
- **Privacy-First:** No data leaves the local machine
- **Performance:** Use SQLite for fast local queries
- **Multi-Browser:** Chrome, Firefox, and Edge support

---

## Testing Guidelines

- Place tests in `tests/` directory
- Name test files: `test_*.py`
- Use pytest framework
- Create synthetic database fixtures for testing
- Mock browser paths for testing
- Test all three OS paths if platform-specific code is modified
- Test error handling for missing files, permission errors
- Include URL sanitization tests

---

## Tool Naming Conflicts

When adding new tools, avoid naming conflicts with imported functions from `chronicle_mcp.database`:
- Rename tool functions if they conflict (e.g., `get_top_domains` → `list_top_domains`)
- Use aliases when importing: `from chronicle_mcp.database import get_top_domains as db_get_top_domains`
