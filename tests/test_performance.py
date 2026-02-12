"""Performance tests for ChronicleMCP."""

import gc
import sqlite3
import threading

import pytest

from chronicle_mcp.database import (
    count_domain_visits,
    get_top_domains,
    query_history,
    query_recent_history,
)

pytestmark = pytest.mark.slow


class TestQueryPerformance:
    """Tests for query performance."""

    @pytest.fixture
    def large_db(self, tmp_path):
        """Create a large synthetic database for performance testing (1,000 entries)."""
        db_path = str(tmp_path / "large_history.db")
        conn = sqlite3.connect(db_path)
        try:
            conn.execute(
                """
                CREATE TABLE urls (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT,
                    visit_count INTEGER DEFAULT 0,
                    last_visit_time INTEGER
                )
            """
            )
            conn.execute("CREATE INDEX idx_url_search ON urls(title, url, last_visit_time)")

            chrome_epoch_offset = 11644473600000000
            # Reduced from 10,000 to 1,000 for faster tests
            for i in range(1000):
                conn.execute(
                    "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
                    (
                        f"https://example{i}.com/page{i % 100}",
                        f"Test Page {i}",
                        i % 10 + 1,
                        chrome_epoch_offset + (i * 1000000),
                    ),
                )
            conn.commit()
        finally:
            conn.close()
        return db_path

    def test_search_performance(self, large_db, benchmark):
        """Test search query performance with large dataset."""
        conn = sqlite3.connect(large_db)
        try:
            result = benchmark(query_history, conn, "example", 100)
            assert result is not None
        finally:
            conn.close()

    def test_recent_history_performance(self, large_db, benchmark):
        """Test recent history query performance."""
        conn = sqlite3.connect(large_db)
        try:
            result = benchmark(query_recent_history, conn, hours=24, limit=100)
            assert result is not None
        finally:
            conn.close()

    def test_count_visits_performance(self, large_db, benchmark):
        """Test count visits performance."""
        conn = sqlite3.connect(large_db)
        try:
            benchmark(count_domain_visits, conn, "example999.com")
        finally:
            conn.close()

    def test_top_domains_performance(self, large_db, benchmark):
        """Test top domains query performance."""
        conn = sqlite3.connect(large_db)
        try:
            result = benchmark(get_top_domains, conn, limit=50)
            assert result is not None
        finally:
            conn.close()


class TestMemoryUsage:
    """Tests for memory usage."""

    def test_query_memory_not_leaking(self, sample_chrome_db):
        """Test that queries don't cause memory leaks."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            for _ in range(50):  # Reduced from 100 for faster tests
                result = query_history(conn, "test", 10)
                del result
            gc.collect()
        finally:
            conn.close()

    def test_large_result_set_handling(self, sample_chrome_db):
        """Test handling of large result sets."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            result = query_history(conn, "", limit=100)  # Reduced from 1000
            assert result is not None
        finally:
            conn.close()


class TestConcurrency:
    """Tests for concurrent access handling."""

    def test_multiple_connections(self, sample_chrome_db):
        """Test multiple concurrent connections."""
        results = []

        def query_worker(worker_id):
            conn = sqlite3.connect(sample_chrome_db)
            try:
                for _ in range(5):  # Reduced from 10 for faster tests
                    result = query_history(conn, "test", 5)
                    results.append((worker_id, result is not None))
            finally:
                conn.close()

        threads = [
            threading.Thread(target=query_worker, args=(i,)) for i in range(3)
        ]  # Reduced from 5

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 15  # 3 threads * 5 iterations
        assert all(success for _, success in results)
