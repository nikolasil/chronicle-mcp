import hashlib
import json
import logging
from collections.abc import Callable
from datetime import timedelta
from typing import Any

from cachetools import TTLCache

logger = logging.getLogger(__name__)


class QueryCache:
    def __init__(self, ttl_seconds: int = 300, max_size: int = 1000):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cache: TTLCache[str, dict[str, Any]] = TTLCache(max_size, ttl_seconds * 1000)

    def _make_key(self, query_type: str, params: dict[str, Any]) -> str:
        """Create a cache key from query type and parameters."""
        key_data = {"type": query_type, "params": params}
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, query_type: str, params: dict[str, Any]) -> Any | None:
        """Get cached result."""
        key = self._make_key(query_type, params)
        if key in self.cache:
            logger.debug(f"Cache hit for {query_type}")
            return self.cache[key]["result"]
        logger.debug(f"Cache miss for {query_type}")
        return None

    def set(self, query_type: str, params: dict[str, Any], result: Any) -> None:
        """Cache a result."""
        key = self._make_key(query_type, params)
        self.cache[key] = {
            "result": result,
            "cached_at": __import__("datetime").datetime.now(),
        }
        logger.debug(f"Cached result for {query_type}")

    def invalidate(self, query_type: str | None = None) -> None:
        """Invalidate cache entries."""
        if query_type:
            keys_to_remove = [k for k, v in self.cache.items() if v.get("type") == query_type]
            for key in keys_to_remove:
                del self.cache[key]
            logger.info(f"Invalidated {len(keys_to_remove)} cache entries for {query_type}")
        else:
            self.cache.clear()
            logger.info("Cache fully cleared")

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self.cache),
            "max_size": self.cache.maxsize,
            "ttl_seconds": self.ttl.total_seconds(),
        }


default_cache = QueryCache(ttl_seconds=300, max_size=1000)


def cached_query(ttl_seconds: int = 300) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to cache query results."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache = QueryCache(ttl_seconds=ttl_seconds)

        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            cached = cache.get(func.__name__, {"args": str(args), "kwargs": str(kwargs)})
            if cached is not None:
                return cached
            result = await func(*args, **kwargs)
            cache.set(func.__name__, {"args": str(args), "kwargs": str(kwargs)}, result)
            return result

        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            cached = cache.get(func.__name__, {"args": str(args), "kwargs": str(kwargs)})
            if cached is not None:
                return cached
            result = func(*args, **kwargs)
            cache.set(func.__name__, {"args": str(args), "kwargs": str(kwargs)}, result)
            return result

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
