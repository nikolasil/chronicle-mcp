# HTTP API Examples

cURL examples for all ChronicleMCP HTTP API endpoints.

## Table of Contents

- [System Examples](#system-examples)
- [Browser Examples](#browser-examples)
- [History Search Examples](#history-search-examples)
- [History Management Examples](#history-management-examples)
- [Bookmarks Examples](#bookmarks-examples)
- [Downloads Examples](#downloads-examples)

---

## System Examples

### Health Check

```bash
curl http://localhost:8080/health
```

### Readiness Check

```bash
curl http://localhost:8080/ready
```

### Get Metrics

```bash
curl http://localhost:8080/metrics
```

### Get Prometheus Metrics

```bash
curl http://localhost:8080/metrics/prometheus
```

---

## Browser Examples

### List Available Browsers

```bash
curl http://localhost:8080/api/browsers
```

### Get Browser Statistics

```bash
curl -X POST http://localhost:8080/api/stats \
  -H "Content-Type: application/json" \
  -d '{"browser": "chrome"}'
```

---

## History Search Examples

### Search History

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python tutorial", "limit": 10, "browser": "chrome"}'
```

### Search with JSON Output

```bash
curl -X POST http://localhost:8080/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "limit": 10, "format": "json"}'
```

### Get Recent History

```bash
curl -X POST http://localhost:8080/api/recent \
  -H "Content-Type: application/json" \
  -d '{"hours": 24, "limit": 20}'
```

### Get Recent History from Specific Browser

```bash
curl -X POST http://localhost:8080/api/recent \
  -H "Content-Type: application/json" \
  -d '{"hours": 48, "browser": "firefox"}'
```

### Count Visits to Domain

```bash
curl -X POST http://localhost:8080/api/count \
  -H "Content-Type: application/json" \
  -d '{"domain": "github.com"}'
```

### Count Visits with Specific Browser

```bash
curl -X POST http://localhost:8080/api/count \
  -H "Content-Type: application/json" \
  -d '{"domain": "stackoverflow.com", "browser": "chrome"}'
```

### Get Top Domains

```bash
curl -X POST http://localhost:8080/api/top-domains \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}'
```

### Get Most Visited Pages

```bash
curl -X POST http://localhost:8080/api/most-visited \
  -H "Content-Type: application/json" \
  -d '{"limit": 20}'
```

### Search by Date Range

```bash
curl -X POST http://localhost:8080/api/search-date \
  -H "Content-Type: application/json" \
  -d '{
    "query": "python",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "limit": 10
  }'
```

### Search by Domain

```bash
curl -X POST http://localhost:8080/api/domain-search \
  -H "Content-Type: application/json" \
  -d '{"domain": "github.com", "query": "issues", "limit": 20}'
```

### Advanced Search with Regex

```bash
curl -X POST http://localhost:8080/api/advanced-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "github\\.com/user/\\w+",
    "use_regex": true,
    "sort_by": "date"
  }'
```

### Advanced Search with Fuzzy Matching

```bash
curl -X POST http://localhost:8080/api/advanced-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "pythn",  # Typo - fuzzy will match "python"
    "use_fuzzy": true,
    "fuzzy_threshold": 0.6
  }'
```

### Advanced Search with Exclusions

```bash
curl -X POST http://localhost:8080/api/advanced-search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "tutorial",
    "exclude_domains": ["ads.example.com", "tracking.example.com"],
    "sort_by": "visit_count"
  }'
```

---

## History Management Examples

### Preview Delete (Dry Run)

```bash
curl -X POST http://localhost:8080/api/delete \
  -H "Content-Type: application/json" \
  -d '{"query": "spam.com", "limit": 100, "confirm": false}'
```

### Delete History Entries

```bash
curl -X POST http://localhost:8080/api/delete \
  -H "Content-Type: application/json" \
  -d '{"query": "spam.com", "limit": 100, "confirm": true}'
```

### Sync History Preview (Dry Run)

```bash
curl -X POST http://localhost:8080/api/sync \
  -H "Content-Type: application/json" \
  -d '{
    "source_browser": "chrome",
    "target_browser": "firefox",
    "dry_run": true
  }'
```

### Sync History with Combine Strategy

```bash
curl -X POST http://localhost:8080/api/sync \
  -H "Content-Type: application/json" \
  -d '{
    "source_browser": "chrome",
    "target_browser": "firefox",
    "merge_strategy": "combine",
    "dry_run": false
  }'
```

### Export History as CSV

```bash
curl -X POST http://localhost:8080/api/export \
  -H "Content-Type: application/json" \
  -d '{"format_type": "csv", "limit": 1000}' \
  --output history.csv
```

### Export History as JSON

```bash
curl -X POST http://localhost:8080/api/export \
  -H "Content-Type: application/json" \
  -d '{"format_type": "json", "limit": 100}' \
  --output history.json
```

---

## Bookmarks Examples

### List Browsers with Bookmarks

```bash
curl http://localhost:8080/api/bookmarks
```

### Query Bookmarks

```bash
curl -X POST http://localhost:8080/api/bookmarks/query \
  -H "Content-Type: application/json" \
  -d '{"query": "python", "limit": 50}'
```

### Query Bookmarks from Specific Browser

```bash
curl -X POST http://localhost:8080/api/bookmarks/query \
  -H "Content-Type: application/json" \
  -d '{"browser": "firefox", "limit": 20}'
```

### Query Bookmarks with JSON Output

```bash
curl -X POST http://localhost:8080/api/bookmarks/query \
  -H "Content-Type: application/json" \
  -d '{"query": "docs", "format": "json"}'
```

---

## Downloads Examples

### List Browsers with Downloads

```bash
curl http://localhost:8080/api/downloads
```

### Query Downloads

```bash
curl -X POST http://localhost:8080/api/downloads/query \
  -H "Content-Type: application/json" \
  -d '{"query": "pdf", "limit": 50}'
```

### Query Downloads from Specific Browser

```bash
curl -X POST http://localhost:8080/api/downloads/query \
  -H "Content-Type: application/json" \
  -d '{"browser": "chrome", "limit": 20}'
```

### Query Downloads with JSON Output

```bash
curl -X POST http://localhost:8080/api/downloads/query \
  -H "Content-Type: application/json" \
  -d '{"query": "document", "format": "json"}'
```

---

## See Also

- [API Overview](../API_INDEX.md)
- [API Endpoints Reference](../API_ENDPOINTS.md)
- [CLI Reference](CLI.md)