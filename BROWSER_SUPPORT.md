# Browser Support Guide

## Table of Contents

1. [Supported Browsers](#supported-browsers)
2. [Chrome](#chrome)
3. [Firefox](#firefox)
4. [Edge](#edge)
5. [Brave](#brave)
6. [Safari](#safari)
7. [Vivaldi](#vivaldi)
8. [Opera](#opera)
9. [Platform Availability](#platform-availability)

---

## Supported Browsers

| Browser | Status | Schema |
|---------|--------|--------|
| Chrome | ✅ Supported | Chrome |
| Firefox | ✅ Supported | Firefox |
| Edge | ✅ Supported | Chrome |
| Brave | ✅ Supported | Chrome |
| Safari | ✅ Supported | Safari |
| Vivaldi | ✅ Supported | Chrome |
| Opera | ✅ Supported | Chrome |

---

## Chrome

### Paths

| Platform | Path |
|----------|------|
| Windows | `%LocalAppData%\Google\Chrome\User Data\Default\History` |
| macOS | `~/Library/Application Support/Google/Chrome/Default/History` |
| Linux | `~/.config/google-chrome/Default/History` |

### Database Schema

- **Table**: `urls`
- **Columns**: `title`, `url`, `last_visit_time` (microseconds since 1601-01-01)
- **Visit Count**: `visit_count`

### Example

```python
search_history("python", browser="chrome")
```

---

## Firefox

### Paths

| Platform | Path |
|----------|------|
| Windows | `%AppData%\Mozilla\Firefox\Profiles\*.default\places.sqlite` |
| macOS | `~/Library/Mozilla/Firefox/Profiles/*.default/places.sqlite` |
| Linux | `~/.mozilla/firefox/*.default/places.sqlite` |

### Database Schema

- **Tables**: `moz_places`, `moz_visits`
- **Columns**: `title`, `url` (from moz_places), `visit_date` (microseconds since 1970-01-01)

### Example

```python
search_history("documentation", browser="firefox")
```

---

## Edge

### Paths

| Platform | Path |
|----------|------|
| Windows | `%LocalAppData%\Microsoft\Edge\User Data\Default\History` |
| macOS | `~/Library/Application Support/Microsoft Edge/Default/History` |
| Linux | `~/.config/microsoft-edge/Default/History` |

### Database Schema

Chrome-based schema (same as Chrome).

### Example

```python
search_history("microsoft docs", browser="edge")
```

---

## Brave

### Paths

| Platform | Path |
|----------|------|
| Windows | `%LocalAppData%\BraveSoftware\Brave-Default\History` |
| macOS | `~/Library/Application Support/BraveSoftware/Brave-Default/History` |
| Linux | `~/.config/BraveSoftware/Brave-Default/History` |

### Database Schema

Chrome-based schema (same as Chrome).

### Example

```python
search_history("privacy", browser="brave")
```

---

## Safari

### Paths

| Platform | Path |
|----------|------|
| macOS | `~/Library/Safari/History.db` |

### Database Schema

- **Tables**: `history_items`, `history_visits`
- **Columns**: `title`, `url` (from history_items), `visit_time` (seconds since 2001-01-01)

### Limitations

- Only available on macOS
- Browser must be closed to access the database

### Example

```python
search_history("apple", browser="safari")
```

---

## Vivaldi

### Paths

| Platform | Path |
|----------|------|
| Windows | `%LocalAppData%\Vivaldi\Default\History` |
| macOS | `~/Library/Application Support/Vivaldi/Default/History` |
| Linux | `~/.config/vivaldi/Default/History` |

### Database Schema

Chrome-based schema (same as Chrome).

### Example

```python
search_history("vivaldi", browser="vivaldi")
```

---

## Opera

### Paths

| Platform | Path |
|----------|------|
| Windows | `%AppData%\Opera Software\Opera Stable\History` |
| macOS | `~/Library/Application Support/com.operasoftware.Opera/History` |
| Linux | `~/.config/opera/History` |

### Database Schema

Chrome-based schema (same as Chrome).

### Example

```python
search_history("opera", browser="opera")
```

---

## Platform Availability

| Browser | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Chrome | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Brave | ✅ | ✅ | ✅ |
| Safari | ❌ | ✅ | ❌ |
| Vivaldi | ✅ | ✅ | ✅ |
| Opera | ✅ | ✅ | ✅ |

---

## Troubleshooting

### Browser Not Found

```bash
# List available browsers
chronicle-mcp list-browsers

# Check browser paths
chronicle-mcp doctor
```

### Database Locked

```bash
# Close the browser before querying
# On Windows, ensure browser process is not running
```

### Permission Denied

```bash
# Check file permissions
ls -la ~/.config/google-chrome/Default/History

# On Linux, you may need to chmod the file
chmod 644 ~/.config/google-chrome/Default/History
```

### Multiple Profiles

ChronicleMCP uses the default profile. For other profiles, specify the path manually:

```python
# Using direct path for non-default profile
from chronicle_mcp.connection import get_history_connection
from chronicle_mcp.database import query_history

with get_history_connection("/path/to/profile/History") as conn:
    results = query_history(conn, "query", 10)
```
