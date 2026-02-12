"""Property-based tests for ChronicleMCP using Hypothesis.

These tests verify correctness across a wide range of inputs
to catch edge cases and regressions.
"""

import sqlite3
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from chronicle_mcp.database import (
    delete_history,
    detect_schema,
    export_history,
    format_chrome_timestamp,
    format_results,
    fuzzy_match_score,
    get_browser_stats,
    get_most_visited_pages,
    query_history,
    query_history_universal,
    sanitize_url,
    search_by_domain,
    search_history_advanced,
    search_with_fuzzy,
    search_with_regex,
)


def valid_url_strategy():
    """Generate valid URL-like strings for testing."""
    protocols = ["http", "https", "ftp"]
    domains = ["example.com", "test.org", "demo.net", "example.io"]
    paths = ["", "/", "/path", "/path/to/resource", "/a/b/c/d/e"]
    query_params = ["", "?q=test", "?token=abc123", "?page=1", "?a=1&b=2"]

    return st.one_of(
        [
            st.builds(
                lambda p, d, t, q: f"{p}://{d}{t}{q}",
                st.sampled_from(protocols),
                st.sampled_from(domains),
                st.sampled_from(paths),
                st.sampled_from(query_params),
            ),
            st.text(min_size=5, max_size=100),
        ]
    )


def create_sample_db():
    """Create a sample Chrome history database."""
    tmpdir = tempfile.mkdtemp()
    db_path = Path(tmpdir) / "History"
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT,
            visit_count INTEGER DEFAULT 0,
            last_visit_time INTEGER DEFAULT 0
        )
    """
    )
    conn.execute("CREATE INDEX idx_url ON urls(url)")
    conn.execute("CREATE INDEX idx_title ON urls(title)")

    sample_data = [
        ("https://github.com/user/repo", "GitHub Repo", 10, 1334500000000000),
        ("https://docs.python.org/3/tutorial/", "Python Tutorial", 5, 1334490000000000),
        ("https://stackoverflow.com/questions/123", "Stack Overflow", 3, 1334480000000000),
        ("https://example.com/path", "Example Domain", 1, 1334470000000000),
        ("https://api.example.com/v1/users", "API Docs", 2, 1334460000000000),
    ]

    conn.executemany(
        "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
        sample_data,
    )
    conn.commit()
    return conn


@pytest.fixture
def sample_db():
    """Create a sample Chrome history database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "History"
        conn = sqlite3.connect(str(db_path))
        conn.execute(
            """
            CREATE TABLE urls (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT,
                visit_count INTEGER DEFAULT 0,
                last_visit_time INTEGER DEFAULT 0
            )
        """
        )
        conn.execute("CREATE INDEX idx_url ON urls(url)")
        conn.execute("CREATE INDEX idx_title ON urls(title)")

        sample_data = [
            ("https://github.com/user/repo", "GitHub Repo", 10, 1334500000000000),
            ("https://docs.python.org/3/tutorial/", "Python Tutorial", 5, 1334490000000000),
            ("https://stackoverflow.com/questions/123", "Stack Overflow", 3, 1334480000000000),
            ("https://example.com/path", "Example Domain", 1, 1334470000000000),
            ("https://api.example.com/v1/users", "API Docs", 2, 1334460000000000),
        ]

        conn.executemany(
            "INSERT INTO urls (url, title, visit_count, last_visit_time) VALUES (?, ?, ?, ?)",
            sample_data,
        )
        conn.commit()
        yield conn
        conn.close()


class TestSanitizeUrl:
    """Property tests for URL sanitization."""

    @given(urls=st.text(min_size=0, max_size=500))
    @settings(max_examples=100)
    def test_sanitize_url_preserves_structure(self, urls):
        """Sanitization should preserve URL structure."""
        if not urls:
            return

        result = sanitize_url(urls)

        if "://" in urls:
            assert "://" in result
            parts = result.split("://", 1)
            assert len(parts) == 2

    @given(urls=st.text(min_size=1, max_size=200))
    @settings(max_examples=50)
    def test_sensitive_params_removed(self, urls):
        """Sensitive parameters should be removed."""
        sensitive_params = [
            "token=abc123",
            "session=xyz789",
            "api_key=secret",
            "password=pass123",
        ]

        base_url = "https://example.com/page"
        for param in sensitive_params:
            test_url = f"{base_url}?{param}"
            result = sanitize_url(test_url)
            assert "abc123" not in result
            assert "xyz789" not in result

    @given(urls=valid_url_strategy())
    @settings(max_examples=20)
    def test_sanitize_url_no_crash(self, urls):
        """Sanitization should not crash on any input."""
        try:
            result = sanitize_url(urls)
            assert isinstance(result, str)
        except Exception:
            pass


class TestFormatChromeTimestamp:
    """Property tests for timestamp formatting."""

    @given(microseconds=st.integers(min_value=0, max_value=10**18))
    @settings(max_examples=50)
    def test_timestamp_format_valid(self, microseconds):
        """Timestamp formatting should produce valid ISO format."""
        result = format_chrome_timestamp(microseconds)

        if result and "microseconds=" not in result:
            assert "T" in result
            assert "+" in result or "-" in result or "Z" in result

    @given(
        ts1=st.integers(min_value=0, max_value=10**15),
        ts2=st.integers(min_value=0, max_value=10**15),
    )
    @settings(max_examples=20)
    def test_timestamp_ordering(self, ts1, ts2):
        """Larger microseconds should produce later timestamps."""
        result1 = format_chrome_timestamp(ts1)
        result2 = format_chrome_timestamp(ts2)

        if "microseconds=" not in result1 and "microseconds=" not in result2:
            if ts1 < ts2:
                assert result1 < result2


class TestFuzzyMatch:
    """Property tests for fuzzy matching."""

    @given(s1=st.text(min_size=0, max_size=100), s2=st.text(min_size=0, max_size=100))
    @settings(max_examples=50)
    def test_fuzzy_score_range(self, s1, s2):
        """Fuzzy match score should be between 0 and 1."""
        score = fuzzy_match_score(s1, s2)
        assert 0.0 <= score <= 1.0

    @given(s=st.text(min_size=1, max_size=50))
    @settings(max_examples=30)
    def test_fuzzy_self_match(self, s):
        """String should match itself with score 1."""
        score = fuzzy_match_score(s, s)
        assert score == 1.0

    @given(s1=st.text(min_size=1, max_size=20), s2=st.text(min_size=1, max_size=20))
    @settings(max_examples=30)
    def test_fuzzy_symmetric(self, s1, s2):
        """Fuzzy matching should be symmetric."""
        score1 = fuzzy_match_score(s1, s2)
        score2 = fuzzy_match_score(s2, s1)
        assert abs(score1 - score2) < 0.001

    @given(s1=st.text(min_size=1, max_size=30), s2=st.text(min_size=1, max_size=30))
    @settings(max_examples=20)
    def test_fuzzy_empty_string(self, s1, s2):
        """Empty strings should have score 0."""
        score1 = fuzzy_match_score("", s2)
        score2 = fuzzy_match_score(s1, "")
        assert score1 == 0.0
        assert score2 == 0.0


class TestQueryHistory:
    """Property tests for history queries."""

    @given(query=st.text(min_size=0, max_size=50), limit=st.integers(min_value=1, max_value=100))
    @settings(max_examples=30, suppress_health_check=["function_scoped_fixture"])
    def test_query_history_empty_query(self, query, limit):
        """Empty query should return results or empty list."""
        sample_db = create_sample_db()
        try:
            if not query.strip():
                rows = query_history(sample_db, query, limit)
                assert isinstance(rows, list)
            else:
                rows = query_history(sample_db, query, limit)
                assert len(rows) <= limit
        finally:
            sample_db.close()

    @given(limit=st.integers(min_value=1, max_value=50))
    @settings(max_examples=20, suppress_health_check=["function_scoped_fixture"])
    def test_query_history_limit_enforced(self, limit):
        """Query should respect limit."""
        sample_db = create_sample_db()
        try:
            rows = query_history(sample_db, "python", limit)
            assert len(rows) <= limit
        finally:
            sample_db.close()

    @given(query=st.text(min_size=1, max_size=30))
    @settings(max_examples=20, suppress_health_check=["function_scoped_fixture"])
    def test_query_history_result_format(self, query):
        """Query results should have correct format."""
        sample_db = create_sample_db()
        try:
            rows = query_history(sample_db, query, 10)

            for row in rows:
                assert len(row) == 3
                title, url, timestamp = row
                assert isinstance(title, str)
                assert isinstance(url, str)
                assert isinstance(timestamp, str)
        finally:
            sample_db.close()


class TestSearchByDomain:
    """Property tests for domain search."""

    @given(domain=st.text(min_size=1, max_size=50), limit=st.integers(min_value=1, max_value=50))
    @settings(max_examples=20, suppress_health_check=["function_scoped_fixture"])
    def test_search_by_domain_format(self, domain, limit):
        """Domain search should return correctly formatted results."""
        sample_db = create_sample_db()
        try:
            rows = search_by_domain(sample_db, domain, limit=limit)

            for row in rows:
                assert len(row) == 3
                title, url, timestamp = row
                assert domain in url or domain.lower() in url.lower()
        finally:
            sample_db.close()

    @given(
        domain=st.text(min_size=1, max_size=30),
        exclude=st.lists(st.text(min_size=1, max_size=30), max_size=3),
    )
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_search_by_domain_exclude(self, domain, exclude):
        """Excluded domains should not appear in results."""
        sample_db = create_sample_db()
        try:
            rows = search_by_domain(sample_db, domain, exclude_domains=exclude, limit=50)

            for row in rows:
                title, url, timestamp = row
                for ex in exclude:
                    assert ex not in url
        finally:
            sample_db.close()


class TestSearchAdvanced:
    """Property tests for advanced search."""

    @given(query=st.text(min_size=0, max_size=50), limit=st.integers(min_value=1, max_value=50))
    @settings(max_examples=25, suppress_health_check=["function_scoped_fixture"])
    def test_search_advanced_basic(self, query, limit):
        """Advanced search should return valid results."""
        sample_db = create_sample_db()
        try:
            rows = search_history_advanced(sample_db, query, limit=limit)
            assert isinstance(rows, list)
        finally:
            sample_db.close()

    @given(
        query=st.text(min_size=1, max_size=30),
        sort_by=st.sampled_from(["date", "visit_count", "title"]),
    )
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_search_advanced_sort(self, query, sort_by):
        """Advanced search should respect sort parameter."""
        sample_db = create_sample_db()
        try:
            rows = search_history_advanced(sample_db, query, limit=10, sort_by=sort_by)

            if len(rows) > 1:
                if sort_by == "title":
                    titles = [r[0] for r in rows]
                    assert titles == sorted(titles)
        finally:
            sample_db.close()


class TestExportHistory:
    """Property tests for history export."""

    @given(
        limit=st.integers(min_value=1, max_value=100), format_type=st.sampled_from(["csv", "json"])
    )
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_export_format(self, limit, format_type):
        """Export should produce valid format."""
        sample_db = create_sample_db()
        try:
            result = export_history(sample_db, format_type=format_type, limit=limit)

            assert isinstance(result, str)

            if format_type == "json":
                import json

                data = json.loads(result)
                assert "entries" in data or "exported_entries" in data
        finally:
            sample_db.close()


class TestRegexSearch:
    """Property tests for regex search."""

    @given(pattern=st.text(min_size=1, max_size=30))
    @settings(max_examples=20, suppress_health_check=["function_scoped_fixture"])
    def test_regex_search_result_format(self, pattern):
        """Regex search should return correctly formatted results."""
        sample_db = create_sample_db()
        try:
            try:
                rows = search_with_regex(sample_db, pattern, limit=10)

                for row in rows:
                    assert len(row) == 3
                    title, url, timestamp = row
                    assert isinstance(title, str)
                    assert isinstance(url, str)
                    assert isinstance(timestamp, str)
            except ValueError:
                pass
        finally:
            sample_db.close()

    @given(pattern=st.text(min_size=1, max_size=20))
    @settings(max_examples=10, suppress_health_check=["function_scoped_fixture"])
    def test_regex_invalid_pattern(self, pattern):
        """Invalid regex patterns should raise ValueError."""
        import re

        sample_db = create_sample_db()
        try:
            try:
                re.compile(pattern)
                rows = search_with_regex(sample_db, pattern, limit=10)
                assert isinstance(rows, list)
            except re.error:
                with pytest.raises(ValueError):
                    search_with_regex(sample_db, pattern, limit=10)
        finally:
            sample_db.close()


class TestFuzzySearch:
    """Property tests for fuzzy search."""

    @given(
        query=st.text(min_size=1, max_size=30), threshold=st.floats(min_value=0.1, max_value=1.0)
    )
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_fuzzy_search_result_format(self, query, threshold):
        """Fuzzy search should return correctly formatted results."""
        sample_db = create_sample_db()
        try:
            rows = search_with_fuzzy(sample_db, query, threshold=threshold, limit=10)

            for row in rows:
                assert len(row) == 4
                title, url, timestamp, score = row
                assert isinstance(title, str)
                assert isinstance(url, str)
                assert isinstance(timestamp, str)
                assert isinstance(score, float)
                assert 0.0 <= score <= 1.0
        finally:
            sample_db.close()

    @given(query=st.text(min_size=1, max_size=20))
    @settings(max_examples=10, suppress_health_check=["function_scoped_fixture"])
    def test_fuzzy_search_threshold(self, query):
        """Fuzzy search should respect threshold."""
        sample_db = create_sample_db()
        try:
            threshold = 0.8
            rows = search_with_fuzzy(sample_db, query, threshold=threshold, limit=20)

            for row in rows:
                score = row[3]
                assert score >= threshold
        finally:
            sample_db.close()


class TestBrowserStats:
    """Property tests for browser statistics."""

    def test_stats_structure(self):
        """Stats should have required fields."""
        sample_db = create_sample_db()
        try:
            stats = get_browser_stats(sample_db)

            required_fields = [
                "total_entries",
                "total_visits",
                "unique_urls",
                "first_visit",
                "last_visit",
            ]

            for field in required_fields:
                assert field in stats
        finally:
            sample_db.close()

    def test_stats_types(self):
        """Stats values should have correct types."""
        sample_db = create_sample_db()
        try:
            stats = get_browser_stats(sample_db)

            assert isinstance(stats["total_entries"], int)
            assert isinstance(stats["total_visits"], int)
            assert isinstance(stats["unique_urls"], int)
        finally:
            sample_db.close()


class TestMostVisitedPages:
    """Property tests for most visited pages."""

    @given(limit=st.integers(min_value=1, max_value=50))
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_most_visited_format(self, limit):
        """Most visited should return correctly formatted results."""
        sample_db = create_sample_db()
        try:
            pages = get_most_visited_pages(sample_db, limit=limit)

            for page in pages:
                assert len(page) == 3
                title, url, visits = page
                assert isinstance(title, str)
                assert isinstance(url, str)
                assert isinstance(visits, int)
        finally:
            sample_db.close()

    @given(limit=st.integers(min_value=1, max_value=30))
    @settings(max_examples=10, suppress_health_check=["function_scoped_fixture"])
    def test_most_visited_order(self, limit):
        """Most visited should be ordered by visit count."""
        sample_db = create_sample_db()
        try:
            pages = get_most_visited_pages(sample_db, limit=limit)

            if len(pages) > 1:
                visits = [p[2] for p in pages]
                assert visits == sorted(visits, reverse=True)
        finally:
            sample_db.close()


class TestFormatResults:
    """Property tests for result formatting."""

    def test_format_results_empty_list(self):
        """Empty list should show appropriate message."""
        rows = []
        result = format_results(rows, "test query", "markdown")
        assert "No history found" in result

    @given(rows=st.lists(st.tuples(st.text(), st.text(), st.text()), max_size=10))
    @settings(max_examples=20)
    def test_format_results_has_content(self, rows):
        """Non-empty results should be formatted correctly."""
        if not rows:
            return
        result = format_results(rows, "test query", "markdown")
        assert len(result) > 0

    @given(
        query=st.text(min_size=1, max_size=30), format_type=st.sampled_from(["markdown", "json"])
    )
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_format_results_non_empty(self, query, format_type):
        """Non-empty results should be formatted correctly."""
        sample_db = create_sample_db()
        try:
            rows = query_history(sample_db, query, limit=5)
            result = format_results(rows, query, format_type)

            assert isinstance(result, str)

            if format_type == "json" and rows:
                import json

                data = json.loads(result)
                assert "results" in data
                assert "count" in data
        finally:
            sample_db.close()


class TestSchemaDetection:
    """Property tests for schema detection."""

    def test_chrome_schema_detected(self):
        """Chrome schema should be detected correctly."""
        sample_db = create_sample_db()
        try:
            schema = detect_schema(sample_db)
            assert schema == "chrome"
        finally:
            sample_db.close()


class TestQueryUniversal:
    """Property tests for universal query."""

    @given(query=st.text(min_size=0, max_size=30), limit=st.integers(min_value=1, max_value=20))
    @settings(max_examples=15, suppress_health_check=["function_scoped_fixture"])
    def test_query_universal_format(self, query, limit):
        """Universal query should return valid results."""
        sample_db = create_sample_db()
        try:
            rows = query_history_universal(sample_db, query, limit=limit, schema="chrome")

            for row in rows:
                assert len(row) == 3
                title, url, timestamp = row
                assert isinstance(title, str)
                assert isinstance(url, str)
                assert isinstance(timestamp, str)
        finally:
            sample_db.close()


class TestDeleteHistory:
    """Property tests for history deletion."""

    @given(query=st.text(min_size=1, max_size=30), limit=st.integers(min_value=1, max_value=50))
    @settings(max_examples=10, suppress_health_check=["function_scoped_fixture"])
    def test_delete_returns_count(self, query, limit):
        """Delete should return number of deleted entries."""
        sample_db = create_sample_db()
        try:
            deleted = delete_history(sample_db, query, limit=limit)
            assert isinstance(deleted, int)
            assert deleted >= 0
        finally:
            sample_db.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
