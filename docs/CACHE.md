# Cache System Guide

ChronicleMCP includes a built-in caching system to improve performance by caching frequently accessed query results.

## Overview

The cache system is designed to:
- Reduce repeated database queries
- Improve response times for common queries
- Support time-based expiration (TTL)
- Maintain cache statistics

## Configuration

### Default Settings

The default cache is configured in `chronicle_mcp/config.py`:

```python
CacheConfig:
    enabled: bool = True
    ttl: int = 300          # 5 minutes
    max_size: int = 1000    # Maximum entries
    cache_type: str = "memory"  # memory, redis (future)
```

### Custom Configuration

Create a `chronicle-mcp.toml` file:

```toml
[cache]
enabled = true
ttl = 600          # 10 minutes
max_size = 500     # Reduced size
cache_type = "memory"
```

## Cache Query Decorator

The `@cached_query` decorator automatically caches function results:

```python
from chronicle_mcp.cache import cached_query, get_default_cache

@cached_query(ttl=300, cache_type="search")
def expensive_search(query: str, limit: int) -> list[dict]:
    # Your search logic here
    return results
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ttl` | int | 300 | Time-to-live in seconds |
| `cache_type` | str | "memory" | Type of cache (currently only "memory") |
| `key_prefix` | str | None | Prefix for cache keys |

## Cache API

### Basic Operations

```python
from chronicle_mcp.cache import QueryCache

# Create a cache
cache = QueryCache(ttl=300, max_size=1000)

# Set a value
cache.set("my_key", {"data": "value"})

# Get a value
result = cache.get("my_key")

# Invalidate a key
cache.invalidate("my_key")

# Clear all entries of a type
cache.invalidate_by_type("search")

# Get statistics
stats = cache.get_stats()
# Returns: {"hits": 42, "misses": 8, "size": 156, "max_size": 1000}
```

### Global Cache

```python
from chronicle_mcp.cache import get_default_cache

cache = get_default_cache()
cache.set("key", "value")
```

## Cache Key Generation

Cache keys are automatically generated from function parameters:

```python
cache = QueryCache()

# Deterministic key
key1 = cache.make_key("search", query="python", limit=10)

# Different parameters = different key
key2 = cache.make_key("search", query="java", limit=10)

# Order independent
key3 = cache.make_key("search", limit=10, query="python")
# key3 == key1
```

## TTL Expiration

Entries expire after `ttl` seconds:

```python
cache = QueryCache(ttl=60)  # 1 minute TTL

cache.set("temp_data", "value")
# After 60 seconds, this key will return None (cache miss)
```

## Eviction

When `max_size` is reached, the oldest entries are evicted:

```python
cache = QueryCache(max_size=100)

# After 100 entries, oldest entries are automatically removed
cache.set("overflow", "data")
```

## Performance Considerations

### What to Cache

- Frequently accessed data (browser lists)
- Complex queries with large result sets
- Statistics calculations
- Time-invariant data

### What NOT to Cache

- Rapidly changing data
- User-specific queries (unless key includes user ID)
- Very large result sets
- Data with security concerns

## Monitoring

### Cache Statistics

```python
from chronicle_mcp.cache import get_default_cache

cache = get_default_cache()
stats = cache.get_stats()

print(f"Hit rate: {stats['hits'] / (stats['hits'] + stats['misses']):.2%}")
print(f"Size: {stats['size']}/{stats['max_size']}")
```

### Logging

Cache operations are logged at DEBUG level:

```
DEBUG - Cache hit: search:python:10
DEBUG - Cache miss: search:java:10
DEBUG - Cache set: search:python:10
DEBUG - Cache invalidate: search
```

## Thread Safety

The cache implementation is thread-safe for concurrent access.

## See Also

- [Architecture](ARCHITECTURE.md) - System architecture
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Cache-related issues
