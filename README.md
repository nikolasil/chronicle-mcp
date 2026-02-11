# ChronicleMCP: Local Browser History for AI Agents

**ChronicleMCP** is a secure, local-first [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that allows AI agents (like Claude Desktop, Cursor, and IDEs) to search your local browser history.

Instead of the AI "hallucinating" or guessing which documentation you were reading, it can now reference the exact pages you've visited—**without your data ever leaving your machine.**

---

## Features

- **Privacy-First:** Your browser history is read directly from your local SQLite database. No cloud syncing, no data collection.
- **Multi-Browser Support:** Chrome, Firefox, and Edge
- **Multiple Search Tools:** Search by query, date range, domain, or recent history
- **Output Formats:** Markdown (default) or JSON
- **Fast Performance:** Built with Python and SQLite
- **Secure:** URL sanitization removes sensitive query parameters (tokens, sessions)

---

## Supported Browsers

| Browser | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Chrome | %LocalAppData%\Google\Chrome\User Data\Default\History | ~/Library/Application Support/Google/Chrome/Default/History | ~/.config/google-chrome/Default/History |
| Edge | %LocalAppData%\Microsoft\Edge\User Data\Default\History | ~/Library/Application Support/Microsoft Edge/Default/History | ~/.config/microsoft-edge/Default/History |
| Firefox | %AppData%\Mozilla\Firefox\Profiles\*.default\places.sqlite | ~/Library/Mozilla/Firefox/Profiles/*.default/places.sqlite | ~/.mozilla/firefox/*.default/places.sqlite |

---

## Installation

### Prerequisites
- Python 3.10+
- [FastMCP](https://github.com/jlowin/fastmcp)
- Chrome, Firefox, or Edge

### Setup
```bash
git clone https://github.com/nikolasil/chronicle-mcp.git
cd chronicle-mcp
pip install fastmcp
```

---

## Available Tools

### list_available_browsers
Returns a list of browsers with detected history databases on your system.

```python
list_available_browsers() -> str
# Returns: "Available browsers: chrome, firefox"
```

### search_history
Searches browser history for keywords in titles or URLs.

```python
search_history(
    query: str,              # Search term
    limit: int = 5,          # Results 1-100
    browser: str = "chrome", # chrome, edge, or firefox
    format_type: str = "markdown"  # markdown or json
) -> str
```

### get_recent_history
Gets recent browsing history from the last N hours.

```python
get_recent_history(
    hours: int = 24,         # Hours to look back
    limit: int = 20,         # Results 1-100
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

### count_visits
Counts total visits to a specific domain.

```python
count_visits(
    domain: str,            # e.g., "github.com"
    browser: str = "chrome"
) -> str
# Returns: "Visits to 'github.com' in chrome: 42"
```

### list_top_domains
Gets the most visited domains.

```python
list_top_domains(
    limit: int = 10,         # Results 1-50
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

### search_history_by_date
Searches history within a date range.

```python
search_history_by_date(
    query: str,
    start_date: str,         # ISO format: YYYY-MM-DD
    end_date: str,           # ISO format: YYYY-MM-DD
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

---

## Output Formats

### Markdown (Default)
```markdown
- **Python Tutorial**
  URL: https://docs.python.org/3/tutorial/
  Timestamp: 2025-01-15T10:30:00+00:00
```

### JSON
```json
{
  "results": [
    {
      "title": "Python Tutorial",
      "url": "https://docs.python.org/3/tutorial/",
      "timestamp": "2025-01-15T10:30:00+00:00"
    }
  ],
  "count": 1
}
```

---

## Security

- **Local-Only:** All data stays on your machine
- **URL Sanitization:** Sensitive query parameters (tokens, sessions, keys) are automatically removed
- **Temp Files:** History is copied to temporary files that are cleaned up after each query
- **Error Messages:** No sensitive file paths exposed in error messages

---

## Troubleshooting

### "Browser history not found"
- Ensure the browser is installed
- Check that Chrome/Edge isn't currently open (locks the database)
- Run `list_available_browsers()` to see detected browsers

### "Permission denied"
- Check file permissions on the browser's history database
- On Windows, ensure the browser is closed before querying

### Empty results
- Try a more specific search term
- Check the date range for `search_history_by_date`
- Verify the browser has history data

### Performance issues
- Large history databases may take longer to query
- Consider reducing the `limit` parameter

---

## Development

### Running Tests
```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_database.py  # Specific file
pytest -k test_name       # Single test
```

### Development Server
```bash
python server.py dev
```

Launches the MCP Inspector web interface for testing tools manually.

---

## Architecture

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

---

## License

MIT License - See LICENSE file for details.
