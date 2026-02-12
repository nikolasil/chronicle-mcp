# ChronicleMCP

<div align="center">

**Secure, local-first Model Context Protocol (MCP) server for browser history**

[![PyPI Version](https://img.shields.io/pypi/v/chronicle-mcp)](https://pypi.org/project/chronicle-mcp/)
[![License](https://img.shields.io/pypi/l/chronicle-mcp)](https://opensource.org/licenses/MIT/)
[![Tests](https://img.shields.io/github/actions/workflow/status/nikolasil/chronicle-mcp/ci.yml?label=tests)](https://github.com/nikolasil/chronicle-mcp/actions)
[![Coverage](https://img.shields.io/codecov/c/github/nikolasil/chronicle-mcp)](https://codecov.io/gh/nikolasil/chronicle-mcp)

</div>

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
   - [CLI Commands](#cli-commands)
   - [MCP Tools](#mcp-tools)
   - [HTTP API](#http-api)
5. [Configuration](#configuration)
6. [Security & Privacy](#security--privacy)
7. [Supported Browsers](#supported-browsers)
8. [Troubleshooting](#troubleshooting)
9. [Development](#development)
10. [Contributing](#contributing)
11. [License](#license)

---

## Quick Start

```bash
# Install
pip install chronicle-mcp

# Run in stdio mode (for AI agents like Claude, Cursor)
chronicle-mcp run

# Or start an HTTP server
chronicle-mcp serve --port 8080

# Check available browsers
chronicle-mcp list-browsers
```

---

## Features

| Feature | Description |
|---------|-------------|
| 🔒 **Privacy-First** | All data stays on your machine. No cloud sync, no data collection. |
| 🌐 **Multi-Browser** | Chrome, Firefox, and Edge support |
| 🔍 **Multiple Search Tools** | Search by query, date range, domain, or recent history |
| 📊 **Output Formats** | Markdown (default) or JSON |
| ⚡ **Fast Performance** | Built with Python and SQLite |
| 🔐 **Secure** | URL sanitization removes sensitive query parameters |
| 🐳 **Docker Support** | Run as a container |
| 🔧 **CLI Interface** | Full command-line control |
| 🌐 **HTTP API** | RESTful API for integrations |

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
# Pull the latest image
docker pull ghcr.io/nikolasil/chronicle-mcp:latest

# Run the server
docker run -p 8080:8080 ghcr.io/nikolasil/chronicle-mcp
```

### From Source

```bash
git clone https://github.com/nikolasil/chronicle-mcp.git
cd chronicle-mcp
pip install -e .
```

### Homebrew (macOS)

```bash
brew install nikolasil/chronicle-mcp/chronicle-mcp
```

---

## Usage

### CLI Commands

#### `chronicle-mcp run`

Run the MCP server in stdio mode (default for AI agents).

```bash
# Stdio mode (default)
chronicle-mcp run

# SSE mode for HTTP clients
chronicle-mcp run --transport sse --port 8080
```

| Option | Description |
|--------|-------------|
| `--transport` | Transport mode: `stdio` or `sse` |
| `--host` | Host to bind (SSE mode only) |
| `--port` | Port to listen on (SSE mode only) |

#### `chronicle-mcp serve`

Start a long-running HTTP/SSE server.

```bash
# Default (foreground, port 8080)
chronicle-mcp serve

# Custom port
chronicle-mcp serve --port 9000

# Daemon mode
chronicle-mcp serve --port 8080 --daemon

# Different browser
chronicle-mcp serve --browser firefox
```

| Option | Description |
|--------|-------------|
| `--host` | Host to bind (default: `127.0.0.1`) |
| `--port` | Port to listen on (default: `8080`) |
| `--browser` | Default browser (default: `chrome`) |
| `--foreground` | Run in foreground (default: true) |
| `--daemon` | Run as daemon |

#### `chronicle-mcp status`

Check if the server is running.

```bash
chronicle-mcp status --port 8080
```

#### `chronicle-mcp logs`

View server logs.

```bash
chronicle-mcp logs --port 8080 --lines 100
```

#### `chronicle-mcp version`

Show version information.

```bash
chronicle-mcp version
```

#### `chronicle-mcp list-browsers`

List available browsers on the system.

```bash
chronicle-mcp list-browsers
# Output: Available browsers: chrome, edge
```

#### `chronicle-mcp completion`

Generate shell completion scripts.

```bash
# Bash
chronicle-mcp completion bash >> ~/.bashrc

# Zsh
chronicle-mcp completion zsh >> ~/.zshrc

# Fish
chronicle-mcp completion fish > ~/.config/fish/completions/chronicle-mcp.fish
```

---

### MCP Tools

#### `search_history`

Search browser history for keywords in titles or URLs.

```python
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

**Example:**
```python
# Markdown output (default)
search_history("python tutorial", limit=10, browser="chrome")

# JSON output
search_history("github", limit=5, format_type="json")
```

#### `get_recent_history`

Get recent browsing history from the last N hours.

```python
def get_recent_history(
    hours: int = 24,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

**Example:**
```python
# Last 24 hours
get_recent_history(hours=48, limit=20)
```

#### `count_visits`

Count total visits to a specific domain.

```python
def count_visits(
    domain: str,
    browser: str = "chrome"
) -> str
```

**Example:**
```python
count_visits("github.com", browser="chrome")
# Output: Visits to 'github.com' in chrome: 42
```

#### `list_top_domains`

Get the most visited domains.

```python
def list_top_domains(
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

**Example:**
```python
list_top_domains(limit=20)
```

#### `search_history_by_date`

Search history within a date range.

```python
def search_history_by_date(
    query: str,
    start_date: str,  # ISO format: YYYY-MM-DD
    end_date: str,    # ISO format: YYYY-MM-DD
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str
```

**Example:**
```python
search_history_by_date(
    "python",
    start_date="2024-01-01",
    end_date="2024-12-31",
    limit=20
)
```

#### `list_available_browsers`

Returns a list of browsers with detected history databases.

```python
def list_available_browsers() -> str
```

**Example:**
```python
list_available_browsers()
# Output: Available browsers: chrome, edge
```

---

### HTTP API

#### Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness check |
| GET | `/metrics` | Basic metrics |
| GET | `/api/browsers` | List available browsers |
| POST | `/api/search` | Search history |
| POST | `/api/recent` | Recent history |
| POST | `/api/count` | Count domain visits |
| POST | `/api/top-domains` | Top domains |
| POST | `/api/search-date` | Search by date |

#### Request/Response Examples

**POST /api/search**

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python tutorial", "limit": 10, "browser": "chrome", "format": "markdown"}'
```

**Response:**
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

**GET /health**

```bash
curl http://localhost:8080/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "chronicle-mcp",
  "version": "1.1.0",
  "timestamp": "2024-01-15T10:30:00+00:00"
}
```

---

## Configuration

ChronicleMCP can be configured using environment variables or a config file.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHRONICLE_CONFIG` | Path to config file | `~/.config/chronicle-mcp/config.toml` |
| `CHRONICLE_PORT` | Default port | `8080` |
| `CHRONICLE_HOST` | Default host | `127.0.0.1` |
| `CHRONICLE_BROWSER` | Default browser | `chrome` |

### Config File

Create `~/.config/chronicle-mcp/config.toml`:

```toml
[default]
browser = "chrome"
limit = 10
format = "markdown"
log_level = "INFO"
```

---

## Security & Privacy

- **Local-Only:** All data stays on your machine
- **URL Sanitization:** Sensitive query parameters are automatically removed:
  - `token`, `session`, `key`, `password`, `auth`, `sid`, `access_token`
- **Temp Files:** History is copied to temporary files that are cleaned up after each query
- **No Data Collection:** Your browsing data is never sent to any server
- **Error Messages:** No sensitive file paths are exposed

---

## Supported Browsers

| Browser | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Chrome | `%LocalAppData%\Google\Chrome\User Data\Default\History` | `~/Library/Application Support/Google/Chrome/Default/History` | `~/.config/google-chrome/Default/History` |
| Edge | `%LocalAppData%\Microsoft\Edge\User Data\Default\History` | `~/Library/Application Support/Microsoft Edge/Default/History` | `~/.config/microsoft-edge/Default/History` |
| Firefox | `%AppData%\Mozilla\Firefox\Profiles\*.default\places.sqlite` | `~/Library/Mozilla/Firefox/Profiles/*.default/places.sqlite` | `~/.mozilla/firefox/*.default/places.sqlite` |

---

## Troubleshooting

### "Browser history not found"

- Ensure the browser is installed
- Check that Chrome/Edge isn't currently open (locks the database)
- Run `chronicle-mcp list-browsers` to see detected browsers

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
# Run all tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest tests/test_database.py

# Single test
pytest -k test_name

# With coverage
pytest --cov=chronicle_mcp
```

### Development Server

```bash
# Run with MCP Inspector
python server.py dev
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy chronicle_mcp/
```

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for AI agents and developers**

</div>
