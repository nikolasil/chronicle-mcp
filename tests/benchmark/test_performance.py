import pytest
import sqlite3
import json
from chronicle_mcp.database import (
    sanitize_url,
    format_chrome_timestamp,
    format_firefox_timestamp,
    format_safari_timestamp,
    fuzzy_match_score,
    query_history,
    get_top_domains,
    search_with_regex,
    search_with_fuzzy,
)
from chronicle_mcp.core.formatters import (
    format_search_results,
    format_recent_results,
    format_top_domains,
    format_export,
)


@pytest.fixture
def test_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT,
            last_visit_time INTEGER,
            visit_count INTEGER DEFAULT 1
        )
    """)

    sample_urls = [
        ("GitHub", "https://github.com/user/repo", 19500000000000000, 100),
        ("Google Search", "https://google.com/search?q=test", 19500000100000000, 50),
        ("Stack Overflow", "https://stackoverflow.com/questions/123", 19500000200000000, 30),
        ("YouTube", "https://youtube.com/watch?v=video123", 19500000300000000, 200),
        ("Twitter", "https://twitter.com/user/status/123", 19500000400000000, 75),
        ("Facebook", "https://facebook.com/page", 19500000500000000, 40),
        ("Reddit", "https://reddit.com/r/python", 19500000600000000, 60),
        ("LinkedIn", "https://linkedin.com/jobs", 19500000700000000, 25),
        ("Amazon", "https://amazon.com/product/123", 19500000800000000, 150),
        ("Wikipedia", "https://en.wikipedia.org/wiki/Python", 19500000900000000, 80),
    ]

    for title, url, ts, vc in sample_urls:
        conn.execute(
            "INSERT INTO urls (title, url, last_visit_time, visit_count) VALUES (?, ?, ?, ?)",
            (title, url, ts, vc)
        )

    for i in range(100):
        conn.execute(
            "INSERT INTO urls (title, url, last_visit_time, visit_count) VALUES (?, ?, ?, ?)",
            (f"Site {i}", f"https://example{i}.com/page", 19500001000000000 + i * 1000000, 1)
        )

    conn.commit()
    yield conn
    conn.close()


class TestDatabaseBenchmarks:
    def test_sanitize_url_without_token(self, benchmark):
        url = "https://example.com/path?page=1&sort=asc"
        result = benchmark(sanitize_url, url)
        assert result == url

    def test_sanitize_url_with_token(self, benchmark):
        url = "https://example.com/path?token=abc123&page=1"
        result = benchmark(sanitize_url, url)
        assert "token=" not in result
        assert "page=1" in result

    def test_sanitize_url_with_multiple_sensitive_params(self, benchmark):
        url = "https://api.example.com?token=secret&api_key=key123&data=value"
        result = benchmark(sanitize_url, url)
        assert "token=" not in result
        assert "api_key=" not in result
        assert "data=value" in result

    def test_format_chrome_timestamp(self, benchmark):
        timestamp = 14014944000000000
        result = benchmark(format_chrome_timestamp, timestamp)
        assert result.endswith("+00:00")
        assert "-" in result

    def test_format_firefox_timestamp(self, benchmark):
        timestamp = 1700000000000000
        result = benchmark(format_firefox_timestamp, timestamp)
        assert "2023" in result or "2024" in result or "2025" in result

    def test_format_safari_timestamp(self, benchmark):
        timestamp = 750000000
        result = benchmark(format_safari_timestamp, timestamp)
        assert "2024" in result or "2025" in result

    def test_fuzzy_match_score_exact(self, benchmark):
        result = benchmark(fuzzy_match_score, "python", "python")
        assert result == 1.0

    def test_fuzzy_match_score_similar(self, benchmark):
        result = benchmark(fuzzy_match_score, "python", "pythn")
        assert result > 0.7

    def test_fuzzy_match_score_different(self, benchmark):
        result = benchmark(fuzzy_match_score, "python", "java")
        assert result < 0.5

    def test_query_history_basic(self, test_db, benchmark):
        result = benchmark(query_history, test_db, "github", 10)
        assert len(result) > 0

    def test_query_history_no_results(self, test_db, benchmark):
        result = benchmark(query_history, test_db, "nonexistent123", 10)
        assert len(result) == 0

    def test_get_top_domains(self, test_db, benchmark):
        result = benchmark(get_top_domains, test_db, 10)
        assert len(result) > 0

    def test_search_with_regex(self, test_db, benchmark):
        result = benchmark(search_with_regex, test_db, r"https?://.*\.com", 20)
        assert len(result) > 0

    def test_search_with_fuzzy(self, test_db, benchmark):
        result = benchmark(search_with_fuzzy, test_db, "github", 0.6, 10)
        assert isinstance(result, list)


class TestFormatterBenchmarks:
    def test_format_search_results_markdown(self, benchmark):
        rows = [
            ("Test Title", "https://example.com", "2024-01-01T00:00:00+00:00"),
            ("Another Page", "https://example2.com", "2024-01-02T00:00:00+00:00"),
        ]
        result = benchmark(format_search_results, rows, "test", "markdown")
        assert "Test Title" in result

    def test_format_search_results_json(self, benchmark):
        rows = [
            ("Test Title", "https://example.com", "2024-01-01T00:00:00+00:00"),
            ("Another Page", "https://example2.com", "2024-01-02T00:00:00+00:00"),
        ]
        result = benchmark(format_search_results, rows, "test", "json")
        data = json.loads(result)
        assert data["count"] == 2

    def test_format_recent_results_markdown(self, benchmark):
        rows = [
            ("Recent Page", "https://example.com", "2024-01-01T00:00:00+00:00"),
        ]
        result = benchmark(format_recent_results, rows, 24, "markdown")
        assert "Recent Page" in result

    def test_format_top_domains_markdown(self, benchmark):
        domains = [
            ("github.com", 100),
            ("google.com", 80),
            ("youtube.com", 60),
        ]
        result = benchmark(format_top_domains, domains, "markdown")
        assert "github.com" in result

    def test_format_top_domains_json(self, benchmark):
        domains = [
            ("github.com", 100),
            ("google.com", 80),
        ]
        result = benchmark(format_top_domains, domains, "json")
        data = json.loads(result)
        assert len(data["top_domains"]) == 2

    def test_format_export_csv(self, benchmark):
        rows = [
            {"title": "Page 1", "url": "https://example.com", "timestamp": "2024-01-01"},
            {"title": "Page 2", "url": "https://example2.com", "timestamp": "2024-01-02"},
        ]
        result = benchmark(format_export, rows, "csv")
        assert "Page 1" in result

    def test_format_export_json(self, benchmark):
        rows = [
            {"title": "Page 1", "url": "https://example.com", "timestamp": "2024-01-01"},
        ]
        result = benchmark(format_export, rows, "json")
        data = json.loads(result)
        assert data["exported_entries"] == 1

    def test_format_search_results_empty(self, benchmark):
        result = benchmark(format_search_results, [], "test", "markdown")
        assert "No history found" in result
