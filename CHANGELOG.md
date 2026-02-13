# Changelog

All notable changes to ChronicleMCP are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Changed

- **Major Architecture Refactoring**: Restructured codebase with layered architecture
  - New `core/` module with centralized business logic (HistoryService)
  - New `protocols/` module with thin MCP and HTTP adapters
  - Better separation of concerns and maintainability
  
- **CLI Simplification**: Clearer command structure
  - `chronicle-mcp mcp` - Run MCP server (replaces `run`)
  - `chronicle-mcp http` - Run HTTP server (replaces `serve`)
  - `chronicle-mcp mcp --sse` - SSE mode (replaces `--transport sse`)

### Added

- **Service Layer**: Centralized business logic in `HistoryService`
- **Validation Module**: Comprehensive input validation
- **Formatters Module**: Consistent response formatting
- **Exception Hierarchy**: Structured error handling
- **Comprehensive Tests**: 95+ new unit tests for core layer

---

## [1.2.19] - 2025-02-13

### Fixed

- Library dependency issues
- Version handling improvements

---

## [1.2.18] - 2025-02-13

### Fixed

- Library dependency fixes
- Build artifact improvements

---

## [1.2.17] - 2025-02-13

### Fixed

- Naming of build artifacts
- Library dependency updates

---

## [1.2.16] - 2025-02-13

### Changed

- Improved build and release process
- Better cross-platform support

---

## [1.2.15] - 2025-02-13

### Fixed

- Rich library compatibility
- Build system improvements

---

## [1.2.14] - 2025-02-13

### Fixed

- Build configuration for binaries
- Include all files in distributions

---

## [1.2.13] - 2025-02-13

### Fixed

- Platform-specific build issues
- Windows-specific error handling

---

## [1.2.12] - 2025-02-13

### Fixed

- Version update workflow
- Release automation improvements

---

## [1.2.11] - 2025-02-13

### Fixed

- Platform build configuration
- Version handling in CI/CD

---

## [1.2.10] - 2025-02-13

### Fixed

- Release workflow improvements
- Version bumping automation

---

## [1.2.9] - 2025-02-13

### Fixed

- CLI command improvements
- Build process refinements

---

## [1.2.8] - 2025-02-13

### Fixed

- Version field corrections
- CI/CD workflow updates

---

## [1.2.7] - 2025-02-13

### Changed

- Merged release and Homebrew workflows
- Improved version management

---

## [1.2.6] - 2025-02-13

### Fixed

- CI workflow permissions
- Release process improvements

---

## [1.2.5] - 2025-02-13

### Fixed

- Detached HEAD handling in CI
- Release workflow stability

---

## [1.2.4] - 2025-02-13

### Fixed

- pip-audit CVE ignore configuration
- CI workflow improvements

---

## [1.2.3] - 2025-02-13

### Fixed

- Trailing whitespace cleanup
- CI workflow refinements

---

## [1.2.2] - 2025-02-13

### Changed

- Version update workflow improvements
- Better release automation

---

## [1.2.1] - 2025-02-13

### Fixed

- Detached HEAD issue in workflows
- CI/CD stability improvements

---

## [1.2.0] - 2025-02-13

### Added

- **Enhanced CI/CD**: Comprehensive GitHub Actions workflows
  - Automated testing across platforms
  - Security scanning with Trivy and Bandit
  - Automatic Homebrew formula updates
  - Container image builds

### Fixed

- Library dependency management
- Version extraction from git tags
- Build and release automation

---

## [1.1.9] - 2025-02-12

### Fixed

- Version handling improvements
- Build process fixes

---

## [1.1.8] - 2025-02-12

### Fixed

- CI workflow improvements
- Release process fixes

---

## [1.1.7] - 2025-02-12

### Fixed

- Import ordering issues
- Test fixture improvements

---

## [1.1.6] - 2025-02-12

### Fixed

- GitHub Actions workflow errors
- Cross-platform test compatibility

---

## [1.1.5] - 2025-02-12

### Fixed

- Comprehensive documentation updates
- CI workflow improvements

---

## [1.1.4] - 2025-02-12

### Added

- **Webhook Notifications**: Support for webhook callbacks
- **Query Caching**: Improved performance with caching
- **New Browsers**: Added Brave, Safari, Vivaldi, Opera support
- **Advanced Search**: Regex and fuzzy matching support
- **New MCP Tools**: 
  - `delete_history` - Delete history entries
  - `search_by_domain` - Domain-specific search
  - `get_browser_stats` - Browser statistics
  - `get_most_visited_pages` - Most visited pages
  - `export_history` - Export to CSV/JSON
  - `search_history_advanced` - Advanced search options
  - `sync_history` - Sync between browsers

### Fixed

- URL sanitization improvements
- Test coverage expansion (104+ tests)
- Docker multi-platform support

---

## [1.1.3] - 2025-02-12

### Fixed

- Version extraction from tags
- CI workflow improvements

---

## [1.1.2] - 2025-02-12

### Fixed

- Release asset handling
- Binary distribution fixes

---

## [1.1.1] - 2025-02-12

### Fixed

- TestPyPI integration
- Release workflow improvements

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
  - `run` - Run MCP server (stdio or SSE transport)
  - `serve` - Start long-running HTTP server
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

## [1.0.1] - 2024-01-20

### Fixed

- Import issues in test modules
- Mock fixture improvements for browser path detection
- Ruff linting and formatting compliance
- Type hint corrections

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

## [0.1.0] - 2024-01-10

### Added

- **Prototype Release**: Initial proof of concept
- Basic MCP server with shadow copy logic
- SQLite database access
- Browser path detection
- README with usage instructions

---

## Version History Summary

| Version | Release Date | Major Changes |
|---------|-------------|---------------|
| 1.2.19 | 2025-02-13 | Latest stable with CI/CD improvements |
| 1.2.0 | 2025-02-13 | Enhanced CI/CD and release automation |
| 1.1.0 | 2025-02-12 | HTTP server and CLI interface added |
| 1.0.0 | 2024-01-15 | Initial stable release |
| 0.1.0 | 2024-01-10 | Prototype release |

---

## Versioning

ChronicleMCP follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

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

### From 1.1.x to 1.2.x

No breaking changes. Upgrade:

```bash
pip install --upgrade chronicle-mcp
```

### From 1.2.x to Unreleased (Next Version)

**Breaking Changes**:
- CLI commands changed:
  - `chronicle-mcp run` → `chronicle-mcp mcp`
  - `chronicle-mcp serve` → `chronicle-mcp http`
  - `--transport sse` → `--sse`

Update your scripts and automation accordingly.

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
