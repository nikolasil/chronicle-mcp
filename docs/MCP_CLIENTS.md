# MCP Client Integration Guide

This guide explains how to configure ChronicleMCP with various MCP clients including Claude Desktop, Cursor, and other compatible editors.

## Quick Start

ChronicleMCP runs as a local MCP server that provides AI assistants access to your browser history. The server uses stdio communication by default, which is the most secure option since all data stays on your machine.

## Claude Desktop Configuration

### 1. Find the Configuration File

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### 2. Add ChronicleMCP to the MCP Servers Section

```json
{
  "mcpServers": {
    "chronicle": {
      "command": "chronicle-mcp",
      "args": ["mcp"]
    }
  }
}
```

### 3. Restart Claude Desktop

After saving the configuration, restart Claude Desktop to load the new MCP server.

### 4. Verify the Connection

Ask Claude: "What browsers do you have access to?" or "Show me my recent browsing history."

## Cursor Configuration

### 1. Open Cursor Settings

Go to **Settings** → **MCP Servers** (or **AI Settings** → **MCP**)

### 2. Add a New MCP Server

Click **Add MCP Server** and configure:

- **Name:** Chronicle Browser History
- **Command:** `chronicle-mcp`
- **Arguments:** `mcp`
- **Environment:** Leave empty for stdio mode

### 3. Save and Connect

Click **Save** and wait for the connection to establish.

## VS Code with Cline/Copilot

For VS Code extensions that support MCP:

```json
{
  "mcpServers": {
    "chronicle": {
      "command": "chronicle-mcp",
      "args": ["mcp"]
    }
  }
}
```

## SSE Mode (Remote Access)

By default, ChronicleMCP uses stdio mode which only works locally. For remote access or accessing from different machines:

```bash
chronicle-mcp mcp --sse --host 127.0.0.1 --port 8080
```

### SSE Configuration for Claude Desktop

```json
{
  "mcpServers": {
    "chronicle": {
      "command": "chronicle-mcp",
      "args": ["mcp", "--sse", "--host", "127.0.0.1", "--port", "8080"],
      "env": {}
    }
  }
}
```

**Security Warning:** SSE mode exposes your browser history over the network. Use firewall rules or VPN to restrict access.

## Available MCP Tools

Once connected, ChronicleMCP provides these tools:

### Browser Management
- `list_available_browsers` - List browsers with history data
- `list_available_bookmarks` - List browsers with bookmarks
- `list_available_downloads` - List browsers with downloads

### Search Operations
- `search_history` - Search by keyword
- `get_recent_history` - Recent browsing
- `count_visits` - Count visits to a domain
- `list_top_domains` - Most visited domains
- `get_most_visited_pages` - Most visited pages
- `search_history_by_date` - Search by date range
- `search_by_domain` - Search within a domain
- `search_history_advanced` - Advanced search with regex/fuzzy

### History Management
- `delete_history` - Delete matching entries
- `sync_history` - Sync between browsers
- `export_history` - Export to CSV/JSON

### Bookmarks & Downloads
- `get_bookmarks` - Get bookmarks
- `get_downloads` - Get downloads

### Analytics
- `compare_time_periods` - Compare browsing between periods
- `analyze_productivity` - Productivity analysis
- `suggest_categories` - Suggest URL categories
- `export_visualization` - Chart.js compatible data
- `generate_insights_report` - Comprehensive insights

### Real-time Subscriptions
- `subscribe_to_history` - Subscribe to changes
- `unsubscribe_from_history` - Unsubscribe
- `get_subscription_status` - Get subscription status

### Deduplication
- `find_duplicate_history` - Find duplicate entries
- `delete_duplicate_history` - Remove duplicates

## Troubleshooting

### "Command not found" error

Ensure ChronicleMCP is installed:
```bash
pip install chronicle-mcp
```

Or if using pipx:
```bash
pipx install chronicle-mcp
```

### "Connection refused" in SSE mode

Check that the server is running:
```bash
chronicle-mcp status --port 8080
```

### No browsers detected

Make sure you've used the browsers and visited some websites. ChronicleMCP reads existing history, not active browsing sessions.

### Permission denied errors

Some systems require explicit permissions to access browser databases. Ensure your user has read access to browser data directories.

## Security Considerations

1. **Local Only:** stdio mode keeps all data on your machine
2. **URL Sanitization:** Sensitive parameters (tokens, passwords) are automatically removed
3. **No Cloud:** Your browsing data never leaves your machine
4. **Temporary Files:** Browser databases are copied temporarily to avoid locking

## Getting Help

If you encounter issues:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
2. Run `chronicle-mcp list-browsers` to verify detection
3. Check the server logs with `chronicle-mcp logs --port 8080 --lines 50`

## See Also

- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [API.md](API.md) - HTTP API reference
- [CLI.md](CLI.md) - CLI commands
- [SECURITY.md](SECURITY.md) - Security policy
