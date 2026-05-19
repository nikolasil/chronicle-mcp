# Troubleshooting Guide

Common issues and solutions for ChronicleMCP.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Browser Detection Issues](#browser-detection-issues)
- [Database Issues](#database-issues)
- [Permission Issues](#permission-issues)
- [Performance Issues](#performance-issues)
- [Connection Issues](#connection-issues)
- [MCP Server Issues](#mcp-server-issues)
- [HTTP Server Issues](#http-server-issues)

---

## Installation Issues

### Python Version Mismatch

**Problem:** `ERROR: Python version mismatch. Expected Python 3.10+`

**Solution:** Ensure you have Python 3.10 or later installed:

```bash
python --version  # Should show Python 3.10.x or higher
```

### Installation Fails with pip

**Problem:** `pip install -e .` fails with dependency errors

**Solution:**
```bash
pip install --upgrade pip
pip install -e ".[dev]"
```

### Package Not Found

**Problem:** `ModuleNotFoundError: No module named 'chronicle_mcp'`

**Solution:** Reinstall the package:

```bash
pip uninstall chronicle-mcp
pip install -e .
```

---

## Browser Detection Issues

### Browser Not Found

**Problem:** `BrowserNotFoundError: Could not find chrome history`

**Possible Causes:**
1. Browser is not installed
2. Browser path is non-standard
3. No history data exists yet

**Solutions:**

1. List available browsers:
```bash
chronicle-mcp list-browsers
```

2. Check if your browser is in the [supported list](browser_support.md)

3. Ensure you've visited some websites with the browser to create history

### Chrome/Edge History Path Not Found

**Problem:** `BrowserPathNotFoundError: Could not find chrome history at ...`

**Solution:**
1. Verify Chrome/Edge is installed
2. Ensure the browser has been run at least once
3. Check that history database exists at the expected path

**Standard Chrome path (Windows):**
```
%LOCALAPPDATA%\Google\Chrome\User Data\Default\History
```

**Standard Edge path (Windows):**
```
%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History
```

### Firefox Multiple Profiles

**Problem:** Only one Firefox profile is detected when you have multiple

**Solution:** ChronicleMCP currently uses the first profile found. To select a specific profile, consider using a symlink to make your preferred profile the default.

---

## Database Issues

### Database Locked

**Problem:** `DatabaseLockedError: Unable to access chrome history database (locked)`

**Cause:** The browser is currently open, preventing read access.

**Solution:**
1. Close the browser completely
2. Wait a few seconds for the database to be released
3. Try again

### Database Permission Denied

**Problem:** `PermissionError: Permission denied accessing chrome history`

**Cause:** Insufficient permissions to read the database file.

**Solutions:**

**Windows:**
- Run as Administrator
- Check file permissions on the History database file

**macOS/Linux:**
```bash
sudo chown $USER:$USER ~/Library/Application\ Support/Google/Chrome/Default/History
```

### Corrupted Database

**Problem:** `DatabaseError: file is not a database` or `sqlite3.DatabaseError`

**Solution:**
1. ChronicleMCP creates temporary copies of the database, so corruption is rare
2. Try closing all browser instances and restarting
3. If the problem persists, the original database may be corrupted

---

## Permission Issues

### Permission Denied on Windows

**Problem:** `PermissionError` when accessing browser data

**Solutions:**

1. **Run as Administrator:**
```bash
# Run Command Prompt as Administrator
chronicle-mcp list-browsers
```

2. **Check file permissions:**
   - Right-click on the History database file
   - Properties → Security → Check permissions for your user

3. **Check antivirus blocking:**
   - Some antivirus software may block access to browser databases

### WSL Permission Issues

**Problem:** Running in WSL and getting permission errors

**Solution:**
- Ensure Windows files are mounted with correct permissions
- Consider running ChronicleMCP directly on Windows instead

---

## Performance Issues

### Slow Query Response

**Problem:** Queries take very long to return results

**Possible Causes:**
1. Large history database (100K+ entries)
2. Network-mounted filesystems
3. Antivirus scanning

**Solutions:**

1. **Limit results:**
```bash
# Use lower limits for faster responses
curl -X POST http://localhost:8080/api/search \
  -d '{"query": "test", "limit": 5}'
```

2. **Use recent history only:**
```bash
curl -X POST http://localhost:8080/api/recent \
  -d '{"hours": 24, "limit": 10}'
```

3. **Check disk health:**
```bash
# Windows
chkdsk

# Linux
smartctl -a /dev/sda
```

### High Memory Usage

**Problem:** ChronicleMCP using excessive memory

**Solution:** Check for memory leaks in long-running processes:

```bash
# Monitor memory usage
tasklist | findstr python
```

---

## Connection Issues

### HTTP Server Won't Start

**Problem:** `chronicle-mcp http` fails to start

**Solutions:**

1. **Check port availability:**
```bash
# Windows
netstat -ano | findstr :8080

# Linux/macOS
lsof -i :8080
```

2. **Kill existing process:**
```bash
# If another process is using port 8080
taskkill /PID <PID> /F
```

3. **Use different port:**
```bash
chronicle-mcp http --port 9090
```

### Daemon Mode Issues

**Problem:** Server started in daemon mode but can't be stopped

**Solutions:**

1. **Check PID file:**
```bash
cat %TEMP%\chronicle-mcp-8080.pid
```

2. **Kill by PID:**
```bash
# Windows
taskkill /PID <PID> /F

# Linux/macOS
kill <PID>
```

3. **Clean up stale PID file:**
```bash
# If process is no longer running
del %TEMP%\chronicle-mcp-8080.pid
```

---

## MCP Server Issues

### MCP Tools Not Registered

**Problem:** AI assistant doesn't see ChronicleMCP tools

**Solution:**
1. Verify MCP server is running in stdio mode:
```bash
chronicle-mcp mcp
```

2. Check tool registration:
```bash
chronicle-mcp mcp --help
```

### SSE Mode Connection Issues

**Problem:** Can't connect to SSE endpoint

**Solutions:**

1. **Check host binding:**
```bash
chronicle-mcp mcp --sse --host 127.0.0.1 --port 8080
```

2. **Firewall settings:**
   - Ensure localhost is allowed through firewall
   - Check that port 8080 is not blocked

---

## HTTP Server Issues

### CORS Errors

**Problem:** `Access-Control-Allow-Origin` errors in browser

**Solution:** Configure CORS in `chronicle-mcp.toml`:

```toml
[server]
host = "127.0.0.1"
port = 8080

[security]
allowed_origins = ["http://localhost:3000"]
```

### JSON Decode Errors

**Problem:** `422 Unprocessable Entity` when sending JSON

**Solution:** Ensure proper Content-Type header:

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

### Empty Responses

**Problem:** API returns empty results

**Solutions:**

1. **Verify browser has history:**
```bash
chronicle-mcp list-browsers
```

2. **Check query syntax:**
   - Try simple queries first: `{"query": "test"}`
   - Avoid special characters unless using regex

---

## Getting Help

### Enable Debug Logging

Create `chronicle-mcp.toml` with:

```toml
[logging]
level = "DEBUG"
json_format = true
file_path = "chronicle-mcp.log"
```

### Check Version

```bash
chronicle-mcp version
```

### Report Issues

When reporting bugs, include:
1. Output of `chronicle-mcp version`
2. Python version: `python --version`
3. Operating system and version
4. Steps to reproduce
5. Log file contents (if available)

---

## See Also

- [Installation Guide](INSTALL.md)
- [Browser Support](BROWSER_SUPPORT.md)
- [Architecture](ARCHITECTURE.md)
- [GitHub Issues](https://github.com/nikolasil/chronicle-mcp/issues)