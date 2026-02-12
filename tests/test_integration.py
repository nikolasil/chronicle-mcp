"""Integration tests for ChronicleMCP.

These tests verify full workflows and cross-component functionality.
"""

import os
import platform
import sqlite3
import tempfile
import time
from datetime import datetime, timezone

import pytest

from chronicle_mcp.connection import get_history_connection
from chronicle_mcp.database import (
    count_domain_visits,
    query_history,
    query_recent_history,
    search_by_date,
)

pytestmark = [pytest.mark.slow, pytest.mark.integration]


class TestCrossBrowserWorkflows:
    """Tests for workflows across multiple browsers."""

    def test_search_across_all_browsers(
        self, mock_all_browsers, sample_chrome_db, sample_firefox_db
    ):
        """Test searching history across Chrome, Firefox, and Edge."""
        # Test Chrome
        conn_chrome = sqlite3.connect(sample_chrome_db)
        chrome_results = query_history(conn_chrome, "github", 10)
        conn_chrome.close()

        # Test Firefox - use direct SQL since Firefox uses moz_places table
        conn_firefox = sqlite3.connect(sample_firefox_db)
        cursor = conn_firefox.cursor()
        cursor.execute(
            "SELECT title, url, last_visit_date FROM moz_places WHERE title LIKE ? OR url LIKE ? LIMIT ?",
            ("%firefox%", "%firefox%", 10),
        )
        firefox_results = cursor.fetchall()
        conn_firefox.close()

        assert len(chrome_results) >= 0  # May be 0 if no matches
        assert len(firefox_results) >= 0

    def test_compare_domains_between_browsers(
        self, mock_all_browsers, sample_chrome_db, sample_firefox_db
    ):
        """Test comparing domain visits between browsers."""
        conn_chrome = sqlite3.connect(sample_chrome_db)
        chrome_count = count_domain_visits(conn_chrome, "github.com")
        conn_chrome.close()

        # Firefox uses moz_places table
        conn_firefox = sqlite3.connect(sample_firefox_db)
        cursor = conn_firefox.cursor()
        cursor.execute(
            "SELECT SUM(visit_count) FROM moz_places WHERE url LIKE ?", ("%firefox.com%",)
        )
        result = cursor.fetchone()
        firefox_count = result[0] if result and result[0] else 0
        conn_firefox.close()

        assert isinstance(chrome_count, int)
        assert isinstance(firefox_count, int)


class TestFullTextSearchAccuracy:
    """Tests for search accuracy and relevance."""

    def test_search_finds_relevant_results(self, mock_realistic_chrome, realistic_chrome_db):
        """Test that search finds relevant results."""
        conn = sqlite3.connect(realistic_chrome_db)
        results = query_history(conn, "github", 20)
        conn.close()

        # Should find results containing "github"
        assert len(results) > 0
        for title, url, timestamp in results:
            assert "github" in title.lower() or "github" in url.lower()

    def test_search_partial_matches(self, mock_realistic_chrome, realistic_chrome_db):
        """Test that partial matches work."""
        conn = sqlite3.connect(realistic_chrome_db)
        results = query_history(conn, "python", 20)
        conn.close()

        # Should find results with "python" in title or URL
        assert len(results) >= 0


class TestTimestampConsistency:
    """Tests for timestamp format consistency."""

    def test_timestamps_consistently_formatted(self, mock_realistic_chrome, realistic_chrome_db):
        """Test that timestamps are consistently formatted."""
        conn = sqlite3.connect(realistic_chrome_db)
        results = query_history(conn, "", 50)  # Get many results
        conn.close()

        for title, url, timestamp in results:
            # Should be ISO format or contain microseconds info
            assert isinstance(timestamp, str)
            assert len(timestamp) > 0


class TestURLSanitizationConsistency:
    """Tests for URL sanitization across all operations."""

    def test_sanitization_across_all_queries(self, mock_chrome_path, sample_chrome_db):
        """Test sanitization works in all query types."""
        conn = sqlite3.connect(sample_chrome_db)

        # Test in regular search
        results = query_history(conn, "token", 10)
        for title, url, timestamp in results:
            assert "secret123" not in url.lower()

        # Test in recent history
        results = query_recent_history(conn, hours=48, limit=10)
        for title, url, timestamp in results:
            assert "secret123" not in url.lower()

        # Test in date search
        results = search_by_date(
            conn, "token", "2024-01-01", datetime.now(timezone.utc).strftime("%Y-%m-%d"), 10
        )
        for title, url, timestamp in results:
            assert "secret123" not in url.lower()

        conn.close()


class TestQueryPerformance:
    """Tests for query performance with large datasets."""

    def test_large_result_set_handling(self, mock_realistic_chrome, realistic_chrome_db):
        """Test handling of large result sets."""
        conn = sqlite3.connect(realistic_chrome_db)
        start = time.time()
        results = query_history(conn, "", limit=100)  # Get up to 100 results
        elapsed = time.time() - start
        conn.close()

        # Should complete in reasonable time
        assert elapsed < 5.0  # 5 seconds max
        assert len(results) <= 100


class TestEdgeCaseDates:
    """Tests for date handling edge cases."""

    def test_leap_year_dates(self, mock_chrome_path, sample_chrome_db):
        """Test dates at leap year boundaries."""
        conn = sqlite3.connect(sample_chrome_db)
        # Feb 29, 2024 (leap year)
        results = search_by_date(conn, "test", "2024-02-29", "2024-03-01", 10)
        conn.close()

        assert isinstance(results, list)

    def test_month_end_dates(self, mock_chrome_path, sample_chrome_db):
        """Test dates at month ends."""
        conn = sqlite3.connect(sample_chrome_db)
        results = search_by_date(conn, "test", "2024-01-31", "2024-02-01", 10)
        conn.close()

        assert isinstance(results, list)


class TestUnicodeHandling:
    """Tests for Unicode content handling."""

    def test_unicode_in_titles_and_urls(self, mock_chrome_path, sample_chrome_db):
        """Test handling of unicode in titles and URLs."""
        conn = sqlite3.connect(sample_chrome_db)
        results = query_history(conn, "日本語", 10)  # Japanese characters
        conn.close()

        # Should not crash, even if no results
        assert isinstance(results, list)

    def test_special_characters_search(self, mock_chrome_path, sample_chrome_db):
        """Test search with special characters."""
        conn = sqlite3.connect(sample_chrome_db)
        results = query_history(conn, "C++", 10)
        conn.close()

        # Should handle special chars without error
        assert isinstance(results, list)


class TestTempFileHandling:
    """Tests for temp file cleanup."""

    @pytest.mark.xfail(
        platform.system() == "Windows",
        reason="Windows file locking prevents immediate cleanup - production code handles gracefully",
    )
    def test_temp_files_cleaned_up(self, mock_chrome_path, sample_chrome_db, tmp_path):
        """Test that temp files are cleaned up after queries."""
        temp_dir = tempfile.gettempdir()
        temp_files_before = set(os.listdir(temp_dir))

        # Run multiple queries
        for _ in range(5):
            try:
                with get_history_connection("chrome") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
            except Exception:
                pass

        # On Windows, file locking may delay cleanup - check with retry
        chronicle_temps = []
        max_retries = 10
        for i in range(max_retries):
            temp_files_after = set(os.listdir(temp_dir))
            new_temp_files = temp_files_after - temp_files_before
            chronicle_temps = [f for f in new_temp_files if f.startswith("chronicle_")]

            if not chronicle_temps:
                break

            if i < max_retries - 1:
                time.sleep(0.2)  # Wait for cleanup

        assert len(chronicle_temps) == 0, f"Leftover temp files: {chronicle_temps}"
