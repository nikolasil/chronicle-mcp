# ChronicleMCP CLI Reference

This document provides a complete reference for all CLI commands, options, and examples.

## Commands Overview

| Command | Description |
|---------|-------------|
| [run](#chronicle-mcp-run) | Run the MCP server |
| [serve](#chronicle-mcp-serve) | Start a long-running HTTP/SSE server |
| [status](#chronicle-mcp-status) | Check server status |
| [logs](#chronicle-mcp-logs) | View server logs |
| [version](#chronicle-mcp-version) | Show version information |
| [list-browsers](#chronicle-mcp-list-browsers) | List available browsers |
| [completion](#chronicle-mcp-completion) | Generate shell completions |

---

## `chronicle-mcp run`

Run the MCP server in stdio or SSE mode.

### Syntax

```bash
chronicle-mcp run [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--transport` | Choice | `stdio` | Transport mode: `stdio` or `sse` |
| `--host` | String | `127.0.0.1` | Host to bind (SSE mode only) |
| `--port` | Integer | `8080` | Port to listen on (SSE mode only) |

### Examples

```bash
# Run in stdio mode (default for AI agents)
chronicle-mcp run

# Run in SSE mode
chronicle-mcp run --transport sse

# SSE mode with custom port
chronicle-mcp run --transport sse --port 9000

# SSE mode listening on all interfaces
chronicle-mcp run --transport sse --host 0.0.0.0 --port 8080
```

### Use Cases

- **stdio mode**: For AI agents (Claude Desktop, Cursor, etc.)
- **SSE mode**: For HTTP clients or web applications

---

## `chronicle-mcp serve`

Start a long-running HTTP/SSE server as a daemon or in foreground.

### Syntax

```bash
chronicle-mcp serve [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--host` | String | `127.0.0.1` | Host to bind to |
| `--port` | Integer | `8080` | Port to listen on |
| `--browser` | String | `chrome` | Default browser to query |
| `--foreground` | Boolean | `true` | Run in foreground |
| `--daemon` | Boolean | `false` | Run as daemon |

### Examples

```bash
# Default (foreground, port 8080)
chronicle-mcp serve

# Custom port
chronicle-mcp serve --port 9000

# Listen on all interfaces
chronicle-mcp serve --host 0.0.0.0 --port 8080

# Different default browser
chronicle-mcp serve --browser firefox

# Run in background (daemon)
chronicle-mcp serve --port 8080 --daemon

# Full options
chronicle-mcp serve --host 0.0.0.0 --port 8080 --browser chrome --daemon
```

### Daemon Mode

When running in daemon mode:
- A PID file is created at `~/.tmp/chronicle-mcp-<port>.pid`
- Logs are written to `~/.tmp/chronicle-mcp-<port>.log`
- Use `status` to check if the server is running
- Use `logs` to view server output

---

## `chronicle-mcp status`

Check if the ChronicleMCP server is running.

### Syntax

```bash
chronicle-mcp status [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | Integer | `8080` | Port to check |

### Examples

```bash
# Check default port
chronicle-mcp status

# Check custom port
chronicle-mcp status --port 9000
```

### Output

**Server Running:**
```
ChronicleMCP is running (PID: 12345)
```

**Server Not Running:**
```
ChronicleMCP is NOT running (no PID file at /tmp/chronicle-mcp-8080.pid)
```

**Stale PID File:**
```
ChronicleMCP is NOT running (stale PID file, PID: 12345)
```

---

## `chronicle-mcp logs`

View logs from the ChronicleMCP server.

### Syntax

```bash
chronicle-mcp logs [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--port` | Integer | `8080` | Port to get logs from |
| `--lines` | Integer | `50` | Number of lines to show |

### Examples

```bash
# Show last 50 lines (default)
chronicle-mcp logs

# Show last 100 lines
chronicle-mcp logs --lines 100

# Check different server
chronicle-mcp logs --port 9000 --lines 200
```

---

## `chronicle-mcp version`

Show the version of ChronicleMCP.

### Syntax

```bash
chronicle-mcp version
```

### Examples

```bash
chronicle-mcp version
```

### Output

```
ChronicleMCP version: 1.1.0
```

---

## `chronicle-mcp list-browsers`

List available browsers on the system.

### Syntax

```bash
chronicle-mcp list-browsers
```

### Examples

```bash
chronicle-mcp list-browsers
```

### Output

**Browsers Found:**
```
Available browsers:
  - chrome
  - edge
```

**No Browsers Found:**
```
No browsers with history found on this system
```

---

## `chronicle-mcp completion`

Generate shell completion scripts.

### Syntax

```bash
chronicle-mcp completion <SHELL>
```

### Arguments

| Argument | Description |
|----------|-------------|
| `bash` | Generate Bash completion script |
| `zsh` | Generate Zsh completion script |
| `fish` | Generate Fish completion script |

### Examples

```bash
# Bash
chronicle-mcp completion bash >> ~/.bashrc
source ~/.bashrc

# Zsh
chronicle-mcp completion zsh >> ~/.zshrc

# Fish
chronicle-mcp completion fish > ~/.config/fish/completions/chronicle-mcp.fish
```

---

## Environment Variables

These environment variables can be used to configure the CLI:

| Variable | Description | Default |
|----------|-------------|---------|
| `CHRONICLE_PORT` | Default port | `8080` |
| `CHRONICLE_HOST` | Default host | `127.0.0.1` |
| `CHRONICLE_BROWSER` | Default browser | `chrome` |
| `CHRONICLE_CONFIG` | Path to config file | Auto-detected |

### Example

```bash
export CHRONICLE_PORT=9000
export CHRONICLE_BROWSER=firefox
chronicle-mcp serve
```

---

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |

---

## See Also

- [API Documentation](API.md)
- [Installation Guide](INSTALL.md)
- [Architecture](ARCHITECTURE.md)
