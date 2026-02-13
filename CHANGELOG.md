# Changelog

All notable changes to ChronicleMCP are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-02-12

### Added

- **HTTP Server**: New HTTP server with RESTful API endpoints
  - `/health` - Health check endpoint
  - `/ready` - Readiness check endpoint
  - `/metrics` - Basic metrics endpoint
  - `/api/browsers` - List available browsers
  - `/api/search` - Search history endpoint
  - `/api/recent` - Recent history endpoint
  - `/api/count` - Count visits endpoint
  - `/api/top-domains` - Top domains endpoint
  - `/api/search-date` - Search by date endpoint

- **CLI Interface**: Full command-line interface with commands:
  - `mcp` - Run MCP server (stdio or SSE transport)
  - `http` - Start HTTP REST API server
  - `status` - Check server status
  - `logs` - View server logs
  - `version` - Show version
  - `list-browsers` - List available browsers
  - `completion` - Generate shell completions

- **Docker Support**: Multi-stage Alpine-based Docker container
  - Multi-platform support (amd64, arm64)
  - Non-root user for security
- **CI/CD Pipelines**:
  - Binary builds for Windows/Linux/macOS
  - Container builds with GitHub Container Registry
  - Security scanning with Trivy and Bandit
  - Integration tests across platforms

### Changed

- **Improved URL Sanitization**: Enhanced removal of sensitive query parameters
- **Better Error Handling**: Specific error types with helpful messages
- **Improved Timestamp Handling**: Better timezone support
- **Test Coverage**: Expanded from 74 to 104+ tests
- **Realistic Test Data**: Test fixtures now include 100+ entries

### Fixed

- **Temp File Cleanup**: Improved cleanup of temporary database files
- **Connection Management**: Better handling of database locks
- **CLI Parameter Issues**: Fixed serve command parameter naming
- **Import Issues**: Fixed test module mocking

### Security

- Added comprehensive security tests
- URL sanitization improvements
- CORS configuration for HTTP server
- Non-root Docker user

---

## [1.0.0] - 2024-01-15

### Added

- **Initial Release**: Core MCP server functionality
- **MCP Tools**:
  - `search_history` - Search by query
  - `get_recent_history` - Recent history
  - `count_visits` - Count domain visits
  - `list_top_domains` - Top domains
  - `search_history_by_date` - Date-range search
  - `list_available_browsers` - List browsers

- **Multi-Browser Support**:
  - Chrome (Windows, macOS, Linux)
  - Edge (Windows, macOS, Linux)
  - Firefox (Windows, macOS, Linux)

- **Output Formats**:
  - Markdown (default)
  - JSON

- **Core Features**:
  - Privacy-first design (local-only)
  - URL sanitization
  - SQLite-based queries
  - Comprehensive test suite (74 tests)

---

## [Unreleased] - Future

### Planned

- **Additional Browsers**: Safari (macOS) support
- **Authentication**: API key support for HTTP server
- **Rate Limiting**: Request throttling
- **Metrics**: Prometheus-compatible metrics endpoint
- **Browser Extensions**: Chrome/Firefox extensions
- **Additional Installation Methods**:
  - MSI installer (Windows)
  - DEB/RPM packages (Linux)
  - Homebrew (Linux/macOS)

---

## Versioning

ChronicleMCP follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version History

| Version | Release Date | Status |
|---------|-------------|--------|
| 1.1.0 | 2025-02-12 | Current |
| 1.0.0 | 2024-01-15 | Stable |

---

## Upgrading

### From 1.0.x to 1.1.x

No breaking changes. Simply upgrade:

```bash
pip install --upgrade chronicle-mcp
```

New features are opt-in:
- HTTP server: `chronicle-mcp serve`
- CLI tools: `chronicle-mcp --help`

---

## Acknowledgments

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP framework
- [Starlette](https://www.starlette.io/) - ASGI framework
- [Click](https://click.palletsprojects.com/) - CLI framework
- [SQLite](https://www.sqlite.org/) - Database

---

## See Also

- [Changelog Template](https://github.com/olivierlacan/keep-a-changelog)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
