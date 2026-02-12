import json
import sqlite3

from chronicle_mcp.database import (
    count_domain_visits,
    format_results,
    get_top_domains,
    query_history,
    sanitize_url,
)


class TestQueryHistory:
    """Tests for history query functions."""

    def test_query_history_basic(self, sample_chrome_db):
        """Test basic history query returns results."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=5)
            assert len(rows) >= 1
            titles = [r[0] for r in rows]
            assert any("Python" in t for t in titles)
        finally:
            conn.close()

    def test_query_history_no_results(self, sample_chrome_db):
        """Test query with no matches returns empty list."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "nonexistent_xyz_query", limit=5)
            assert rows == []
        finally:
            conn.close()

    def test_query_history_limit(self, sample_chrome_db):
        """Test that limit is respected."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "https", limit=2)
            assert len(rows) <= 2
        finally:
            conn.close()


class TestSanitizeUrl:
    """Tests for URL sanitization."""

    def test_sanitize_url_removes_token(self):
        """Test that sensitive tokens are removed from URLs."""
        url = "https://example.com/page?token=secret123&other=value"
        result = sanitize_url(url)

        assert "token=secret123" not in result
        assert "other=value" in result

    def test_sanitize_url_removes_multiple_sensitive_params(self):
        """Test removal of multiple sensitive parameters."""
        url = "https://example.com/page?token=abc&session=xyz&key=123&name=test"
        result = sanitize_url(url)

        assert "token=" not in result
        assert "session=" not in result
        assert "key=" not in result
        assert "name=test" in result

    def test_sanitize_url_preserves_structure(self):
        """Test that URL structure is preserved after sanitization."""
        url = "https://github.com/user/repo?tab=repos"
        result = sanitize_url(url)

        assert result.startswith("https://")
        assert "github.com" in result


class TestFormatResults:
    """Tests for result formatting."""

    def test_format_results_markdown(self, sample_chrome_db):
        """Test Markdown format output."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=1)
            result = format_results(rows, "python", "markdown")

            assert "- **" in result
            assert "URL:" in result
        finally:
            conn.close()

    def test_format_results_json(self, sample_chrome_db):
        """Test JSON format output."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            rows = query_history(conn, "python", limit=1)
            result = format_results(rows, "python", "json")

            data = json.loads(result)
            assert "results" in data
            assert "count" in data
            assert data["count"] == len(rows)
        finally:
            conn.close()

    def test_format_results_empty(self):
        """Test empty results return not found message."""
        result = format_results([], "nonexistent", "markdown")
        assert "No history found" in result


class TestCountDomainVisits:
    """Tests for domain visit counting."""

    def test_count_domain_visits_basic(self, sample_chrome_db):
        """Test counting visits to a domain."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            count = count_domain_visits(conn, "github.com")
            assert count >= 0
        finally:
            conn.close()

    def test_count_domain_visits_nonexistent(self, sample_chrome_db):
        """Test counting visits to nonexistent domain."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            count = count_domain_visits(conn, "nonexistent.xyz")
            assert count == 0
        finally:
            conn.close()


class TestGetTopDomains:
    """Tests for top domains function."""

    def test_get_top_domains_basic(self, sample_chrome_db):
        """Test getting top domains returns results."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            domains = get_top_domains(conn, limit=5)
            assert isinstance(domains, list)
            if domains:
                assert isinstance(domains[0], tuple)
                assert len(domains[0]) == 2
        finally:
            conn.close()

    def test_get_top_domains_limit(self, sample_chrome_db):
        """Test that limit is respected."""
        conn = sqlite3.connect(sample_chrome_db)
        try:
            domains = get_top_domains(conn, limit=2)
            assert len(domains) <= 2
        finally:
            conn.close()
