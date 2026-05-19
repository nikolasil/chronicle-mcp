# ChronicleMCP

<div align="center">

**Secure, local-first Model Context Protocol (MCP) server for browser history**

[![PyPI Version](https://img.shields.io/pypi/v/chronicle-mcp)](https://pypi.org/project/chronicle-mcp/)
[![License](https://img.shields.io/pypi/l/chronicle-mcp)](https://opensource.org/licenses/MIT/)
[![Tests](https://img.shields.io/github/actions/workflow/status/nikolasil/chronicle-mcp/ci.yml?label=tests)](https://github.com/nikolasil/chronicle-mcp/actions)
[![Coverage](https://img.shields.io/codecov/c/github/nikolasil/chronicle-mcp)](https://codecov.io/gh/nikolasil/chronicle-mcp)

</div>

ChronicleMCP provides AI agents with secure, privacy-first access to local browser history through the Model Context Protocol (MCP). All data stays on your machine.

## Quick Start

```bash
pip install chronicle-mcp

chronicle-mcp mcp              # MCP server (stdio mode)
chronicle-mcp http --port 8080 # HTTP REST API
chronicle-mcp list-browsers    # Detect available browsers
```

## Features

- **Privacy-First**: All data stays on your machine
- **Multi-Browser**: Chrome, Firefox, Edge, Brave, Safari, Vivaldi, Opera
- **Multiple Search Tools**: Query, date range, domain, or recent history
- **Output Formats**: Markdown, JSON, CSV
- **Bookmarks & Downloads**: Access bookmarks and download history
- **Analytics**: Productivity analysis, time period comparison, insights

## Documentation

- [Installation Guide](INSTALL.md)
- [CLI Reference](CLI.md)
- [HTTP API](API.md)
- [Architecture](ARCHITECTURE.md)
- [Browser Support](browser_support.md)
- [Security Hardening](security_hardening.md)

## License

MIT License
