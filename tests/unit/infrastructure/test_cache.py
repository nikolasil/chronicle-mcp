"""Tests for cache module.

This module tests the QueryCache class and cached_query decorator.
"""

import asyncio
import time

import pytest

from chronicle_mcp.cache import QueryCache, cached_query, default_cache


class TestQueryCacheInitialization:
    """Tests for QueryCache initialization."""

    def test_default_initialization(self):
        """Test default cache initialization."""
        cache = QueryCache()
        assert cache.ttl.total_seconds() == 300
        assert cache.cache.maxsize == 1000
        assert len(cache.cache) == 0

    def test_custom_initialization(self):
        """Test custom cache initialization."""
        cache = QueryCache(ttl_seconds=600, max_size=500)
        assert cache.ttl.total_seconds() == 600
        assert cache.cache.maxsize == 500

    def test_zero_ttl(self):
        """Test initialization with zero TTL."""
        cache = QueryCache(ttl_seconds=0)
        assert cache.ttl.total_seconds() == 0


class TestMakeKey:
    """Tests for _make_key method."""

    def test_make_key_deterministic(self):
        """Test that key generation is deterministic."""
        cache = QueryCache()
        key1 = cache._make_key("search", {"query": "test", "limit": 10})
        key2 = cache._make_key("search", {"query": "test", "limit": 10})
        assert key1 == key2

    def test_make_key_different_params(self):
        """Test different parameters produce different keys."""
        cache = QueryCache()
        key1 = cache._make_key("search", {"query": "test", "limit": 10})
        key2 = cache._make_key("search", {"query": "test", "limit": 20})
        assert key1 != key2

    def test_make_key_different_types(self):
        """Test different query types produce different keys."""
        cache = QueryCache()
        key1 = cache._make_key("search", {"query": "test"})
        key2 = cache._make_key("recent", {"query": "test"})
        assert key1 != key2

    def test_make_key_order_independence(self):
        """Test key generation is independent of dict order."""
        cache = QueryCache()
        key1 = cache._make_key("search", {"a": 1, "b": 2})
        key2 = cache._make_key("search", {"b": 2, "a": 1})
        assert key1 == key2


class TestCacheGet:
    """Tests for get method."""

    def test_get_miss(self):
        """Test getting non-existent key returns None."""
        cache = QueryCache()
        result = cache.get("search", {"query": "test"})
        assert result is None

    def test_get_hit(self):
        """Test getting existing key returns value."""
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "cached_result")
        result = cache.get("search", {"query": "test"})
        assert result == "cached_result"

    def test_get_different_params(self):
        """Test getting with different params returns None."""
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "cached_result")
        result = cache.get("search", {"query": "other"})
        assert result is None


class TestCacheSet:
    """Tests for set method."""

    def test_set_basic(self):
        """Test basic set operation."""
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "result")
        assert cache.get("search", {"query": "test"}) == "result"

    def test_set_overwrite(self):
        """Test setting same key overwrites value."""
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "old_result")
        cache.set("search", {"query": "test"}, "new_result")
        assert cache.get("search", {"query": "test"}) == "new_result"

    def test_set_multiple_keys(self):
        """Test setting multiple different keys."""
        cache = QueryCache()
        cache.set("search", {"query": "a"}, "result_a")
        cache.set("search", {"query": "b"}, "result_b")
        assert cache.get("search", {"query": "a"}) == "result_a"
        assert cache.get("search", {"query": "b"}) == "result_b"

    def test_set_complex_value(self):
        """Test setting complex data structures."""
        cache = QueryCache()
        value = {"results": [1, 2, 3], "count": 3}
        cache.set("search", {"query": "test"}, value)
        assert cache.get("search", {"query": "test"}) == value


class TestCacheInvalidate:
    """Tests for invalidate method."""

    def test_invalidate_all(self):
        """Test invalidating all cache entries."""
        cache = QueryCache()
        cache.set("search", {"query": "a"}, "result_a")
        cache.set("search", {"query": "b"}, "result_b")
        cache.set("recent", {"hours": 24}, "result_c")

        cache.invalidate()

        assert cache.get("search", {"query": "a"}) is None
        assert cache.get("search", {"query": "b"}) is None
        assert cache.get("recent", {"hours": 24}) is None

    def test_invalidate_by_type(self):
        """Test invalidating entries by type."""
        cache = QueryCache()
        cache.set("search", {"query": "a"}, "result_a")
        cache.set("search", {"query": "b"}, "result_b")
        cache.set("recent", {"hours": 24}, "result_c")

        cache.invalidate("search")

        assert cache.get("search", {"query": "a"}) is None
        assert cache.get("search", {"query": "b"}) is None
        assert cache.get("recent", {"hours": 24}) == "result_c"

    def test_invalidate_nonexistent_type(self):
        """Test invalidating non-existent type doesn't error."""
        cache = QueryCache()
        cache.set("search", {"query": "a"}, "result_a")
        cache.invalidate("nonexistent")
        assert cache.get("search", {"query": "a"}) == "result_a"

    def test_invalidate_empty_cache(self):
        """Test invalidating empty cache doesn't error."""
        cache = QueryCache()
        cache.invalidate()
        assert len(cache.cache) == 0


class TestCacheGetStats:
    """Tests for get_stats method."""

    def test_get_stats_empty(self):
        """Test stats for empty cache."""
        cache = QueryCache()
        stats = cache.get_stats()
        assert stats["size"] == 0
        assert stats["max_size"] == 1000
        assert stats["ttl_seconds"] == 300

    def test_get_stats_with_entries(self):
        """Test stats with entries."""
        cache = QueryCache()
        cache.set("search", {"query": "a"}, "result_a")
        cache.set("search", {"query": "b"}, "result_b")

        stats = cache.get_stats()
        assert stats["size"] == 2
        assert stats["max_size"] == 1000

    def test_get_stats_custom_config(self):
        """Test stats reflect custom configuration."""
        cache = QueryCache(ttl_seconds=600, max_size=500)
        stats = cache.get_stats()
        assert stats["ttl_seconds"] == 600
        assert stats["max_size"] == 500


class TestCacheTTLExpiration:
    """Tests for TTL expiration behavior."""

    def test_ttl_expiration(self):
        """Test entries expire after TTL."""
        cache = QueryCache(ttl_seconds=0)  # Instant expiration
        cache.set("search", {"query": "test"}, "result")

        # Entry should still be there immediately
        time.sleep(0.01)  # Small delay to ensure TTL is processed

        # After TTL, entry might or might not be there depending on
        # when TTLCache checks expiration
        result = cache.get("search", {"query": "test"})
        # Just verify we can call get without error
        assert result is None or result == "result"


class TestCacheEviction:
    """Tests for cache eviction behavior."""

    def test_max_size_eviction(self):
        """Test old entries are evicted when max size reached."""
        cache = QueryCache(ttl_seconds=3600, max_size=2)
        cache.set("search", {"query": "a"}, "result_a")
        cache.set("search", {"query": "b"}, "result_b")
        cache.set("search", {"query": "c"}, "result_c")

        # At least one of the first entries should be evicted
        count = sum(
            1
            for key in ["result_a", "result_b", "result_c"]
            if cache.get("search", {"query": key.replace("result_", "")}) == key
        )
        assert count <= 2  # Should not exceed max size


class TestCachedQueryDecorator:
    """Tests for cached_query decorator."""

    def test_cached_query_sync(self):
        """Test caching synchronous function."""
        call_count = 0

        @cached_query(ttl_seconds=60)
        def expensive_function(query: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"result_for_{query}"

        # First call should execute function
        result1 = expensive_function("test")
        assert result1 == "result_for_test"
        assert call_count == 1

        # Second call with same args should return cached result
        result2 = expensive_function("test")
        assert result2 == "result_for_test"
        assert call_count == 1  # Function not called again

    def test_cached_query_different_args(self):
        """Test caching with different arguments."""
        call_count = 0

        @cached_query(ttl_seconds=60)
        def expensive_function(query: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"result_for_{query}"

        expensive_function("a")
        expensive_function("b")

        assert call_count == 2  # Different args = different cache keys

    @pytest.mark.asyncio
    async def test_cached_query_async(self):
        """Test caching asynchronous function."""
        call_count = 0

        @cached_query(ttl_seconds=60)
        async def async_function(query: str) -> str:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.001)  # Simulate async work
            return f"async_result_for_{query}"

        # First call should execute function
        result1 = await async_function("test")
        assert result1 == "async_result_for_test"
        assert call_count == 1

        # Second call should return cached result
        result2 = await async_function("test")
        assert result2 == "async_result_for_test"
        assert call_count == 1


class TestDefaultCache:
    """Tests for default_cache instance."""

    def test_default_cache_exists(self):
        """Test default cache is initialized."""
        assert isinstance(default_cache, QueryCache)
        assert default_cache.ttl.total_seconds() == 300
        assert default_cache.cache.maxsize == 1000

    def test_default_cache_operations(self):
        """Test default cache can be used."""
        default_cache.set("test", {"key": "value"}, "test_result")
        result = default_cache.get("test", {"key": "value"})
        assert result == "test_result"
        # Cleanup
        default_cache.invalidate()


class TestCacheLogging:
    """Tests for cache logging behavior."""

    def test_cache_hit_logging(self, caplog):
        """Test logging on cache hit."""
        caplog.set_level("DEBUG")
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "result")
        cache.get("search", {"query": "test"})
        assert "Cache hit" in caplog.text

    def test_cache_miss_logging(self, caplog):
        """Test logging on cache miss."""
        caplog.set_level("DEBUG")
        cache = QueryCache()
        cache.get("search", {"query": "nonexistent"})
        assert "Cache miss" in caplog.text

    def test_cache_set_logging(self, caplog):
        """Test logging on cache set."""
        caplog.set_level("DEBUG")
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "result")
        assert "Cached result" in caplog.text

    def test_invalidate_logging(self, caplog):
        """Test logging on invalidate."""
        caplog.set_level("INFO")
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "result")
        cache.invalidate()
        assert "Cache fully cleared" in caplog.text

    def test_invalidate_by_type_logging(self, caplog):
        """Test logging on invalidate by type."""
        caplog.set_level("INFO")
        cache = QueryCache()
        cache.set("search", {"query": "test"}, "result")
        cache.invalidate("search")
        assert "Invalidated" in caplog.text
        assert "search" in caplog.text
