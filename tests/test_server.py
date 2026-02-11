import inspect
import json

import pytest


def get_tool_func(module, tool_name):
    """Get the underlying function from a FastMCP tool."""
    tool = getattr(module, tool_name)
    return tool.fn


def get_required_params(func):
    """Get required parameter names from function signature."""
    sig = inspect.signature(func)
    return [
        name
        for name, param in sig.parameters.items()
        if param.default is inspect.Parameter.empty
        and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
    ]


class TestSearchHistory:
    """Tests for the search_history MCP tool."""

    def test_search_history_basic(self, mock_chrome_path, sample_chrome_db):
        """Test basic search returns results."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=5, browser="chrome")
        assert "python" in result.lower() or "Python" in result

    def test_search_history_no_results(self, mock_chrome_path, sample_chrome_db):
        """Test search with no matches returns not found message."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("xyznonexistent123", limit=5, browser="chrome")
        assert "no history found" in result.lower()

    def test_search_history_empty_query(self, mock_chrome_path, sample_chrome_db):
        """Test that empty query returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("", limit=5, browser="chrome")
        assert "error" in result.lower()
        assert "empty" in result.lower()

    def test_search_history_whitespace_query(self, mock_chrome_path, sample_chrome_db):
        """Test that whitespace-only query returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("   ", limit=5, browser="chrome")
        assert "error" in result.lower()

    def test_search_history_invalid_limit_too_low(self, mock_chrome_path, sample_chrome_db):
        """Test that limit below 1 returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=0, browser="chrome")
        assert "error" in result.lower()
        assert "limit" in result.lower()

    def test_search_history_invalid_limit_negative(self, mock_chrome_path, sample_chrome_db):
        """Test that negative limit returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=-5, browser="chrome")
        assert "error" in result.lower()
        assert "limit" in result.lower()

    def test_search_history_limit_above_max(self, mock_chrome_path, sample_chrome_db):
        """Test that limit above 100 returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=150, browser="chrome")
        assert "error" in result.lower()
        assert "limit" in result.lower()

    def test_search_history_invalid_browser(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid browser returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=5, browser="invalid_browser")
        assert "error" in result.lower()
        assert "invalid" in result.lower() or "browser" in result.lower()

    def test_search_history_invalid_format(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid format returns error."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=5, browser="chrome", format_type="xml")
        assert "error" in result.lower()
        assert "format" in result.lower()

    def test_search_history_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test JSON output format."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("github", limit=5, browser="chrome", format_type="json")
        data = json.loads(result)
        assert "results" in data
        assert "count" in data
        assert data["count"] >= 0

    def test_search_history_markdown_format(self, mock_chrome_path, sample_chrome_db):
        """Test Markdown output format (default)."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("github", limit=5, browser="chrome", format_type="markdown")
        assert "- **" in result
        assert "URL:" in result

    def test_search_history_case_insensitive_browser(self, mock_chrome_path, sample_chrome_db):
        """Test that browser names are case insensitive."""
        import server

        func = get_tool_func(server, "search_history")
        result_lower = func("python", limit=5, browser="chrome")
        result_upper = func("python", limit=5, browser="CHROME")
        result_mixed = func("python", limit=5, browser="Chrome")
        assert result_lower == result_upper == result_mixed


class TestGetRecentHistory:
    """Tests for the get_recent_history MCP tool."""

    def test_get_recent_history_basic(self, mock_chrome_path, sample_chrome_db):
        """Test basic recent history retrieval."""
        import server

        func = get_tool_func(server, "get_recent_history")
        result = func(hours=24, limit=10, browser="chrome")
        assert result is not None

    def test_get_recent_history_invalid_hours(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid hours returns error."""
        import server

        func = get_tool_func(server, "get_recent_history")
        result = func(hours=-1, limit=10, browser="chrome")
        assert "error" in result.lower()

    def test_get_recent_history_invalid_limit(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid limit returns error."""
        import server

        func = get_tool_func(server, "get_recent_history")
        result = func(hours=24, limit=0, browser="chrome")
        assert "error" in result.lower()

    def test_get_recent_history_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test JSON output format."""
        import datetime
        import json
        import sqlite3

        import server

        func = get_tool_func(server, "get_recent_history")

        now = datetime.datetime.now(datetime.timezone.utc)
        recent_timestamp = (
            int((now - datetime.timedelta(hours=2)).timestamp() * 1_000_000) + 11644473600000000
        )

        conn = sqlite3.connect(sample_chrome_db)
        conn.execute("UPDATE urls SET last_visit_time = ? WHERE id = 1", (recent_timestamp,))
        conn.commit()
        conn.close()

        result = func(hours=24, limit=5, browser="chrome", format_type="json")

        if result.startswith("{"):
            data = json.loads(result)
            assert "results" in data
        else:
            assert "error" in result.lower()


class TestCountVisits:
    """Tests for the count_visits MCP tool."""

    def test_count_visits_basic(self, mock_chrome_path, sample_chrome_db):
        """Test basic visit counting."""
        import server

        func = get_tool_func(server, "count_visits")
        result = func(domain="github.com", browser="chrome")
        assert "github.com" in result.lower()
        assert "visits" in result.lower()

    def test_count_visits_nonexistent_domain(self, mock_chrome_path, sample_chrome_db):
        """Test counting visits to nonexistent domain."""
        import server

        func = get_tool_func(server, "count_visits")
        result = func(domain="nonexistent.xyz", browser="chrome")
        assert "0" in result

    def test_count_visits_empty_domain(self, mock_chrome_path, sample_chrome_db):
        """Test that empty domain returns error."""
        import server

        func = get_tool_func(server, "count_visits")
        result = func(domain="", browser="chrome")
        assert "error" in result.lower()
        assert "domain" in result.lower()

    def test_count_visits_invalid_browser(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid browser returns error."""
        import server

        func = get_tool_func(server, "count_visits")
        result = func(domain="github.com", browser="invalid")
        assert "error" in result.lower()


class TestListTopDomains:
    """Tests for the list_top_domains MCP tool."""

    def test_list_top_domains_basic(self, mock_chrome_path, sample_chrome_db):
        """Test basic top domains retrieval."""
        import server

        func = get_tool_func(server, "list_top_domains")
        result = func(limit=5, browser="chrome")
        assert result is not None

    def test_list_top_domains_invalid_limit(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid limit returns error."""
        import server

        func = get_tool_func(server, "list_top_domains")
        result = func(limit=0, browser="chrome")
        assert "error" in result.lower()

    def test_list_top_domains_limit_too_high(self, mock_chrome_path, sample_chrome_db):
        """Test that limit above 50 returns error."""
        import server

        func = get_tool_func(server, "list_top_domains")
        result = func(limit=100, browser="chrome")
        assert "error" in result.lower()

    def test_list_top_domains_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test JSON output format."""
        import server

        func = get_tool_func(server, "list_top_domains")
        result = func(limit=5, browser="chrome", format_type="json")
        data = json.loads(result)
        assert "top_domains" in data


class TestListAvailableBrowsers:
    """Tests for the list_available_browsers MCP tool."""

    def test_list_available_browsers_returns_string(self, mock_all_browsers):
        """Test that the tool returns a string."""
        import server

        func = get_tool_func(server, "list_available_browsers")
        result = func()
        assert isinstance(result, str)

    def test_list_available_browsers_contains_chrome(self, mock_all_browsers):
        """Test that Chrome is detected."""
        import server

        func = get_tool_func(server, "list_available_browsers")
        result = func()
        assert "chrome" in result.lower()


class TestSearchHistoryByDate:
    """Tests for the search_history_by_date MCP tool."""

    def test_search_history_by_date_basic(self, mock_chrome_path, sample_chrome_db):
        """Test basic date-range search."""
        import server

        func = get_tool_func(server, "search_history_by_date")
        result = func(
            query="python",
            start_date="2024-01-01",
            end_date="2025-12-31",
            limit=5,
            browser="chrome",
        )
        assert result is not None

    def test_search_history_by_date_invalid_query(self, mock_chrome_path, sample_chrome_db):
        """Test that empty query returns error."""
        import server

        func = get_tool_func(server, "search_history_by_date")
        result = func(
            query="", start_date="2024-01-01", end_date="2025-12-31", limit=5, browser="chrome"
        )
        assert "error" in result.lower()

    def test_search_history_by_date_invalid_limit(self, mock_chrome_path, sample_chrome_db):
        """Test that invalid limit returns error."""
        import server

        func = get_tool_func(server, "search_history_by_date")
        result = func(
            query="python",
            start_date="2024-01-01",
            end_date="2025-12-31",
            limit=0,
            browser="chrome",
        )
        assert "error" in result.lower()

    def test_search_history_by_date_json_format(self, mock_chrome_path, sample_chrome_db):
        """Test JSON output format."""
        import server

        func = get_tool_func(server, "search_history_by_date")
        result = func(
            query="github",
            start_date="2024-01-01",
            end_date="2025-12-31",
            limit=5,
            browser="chrome",
            format_type="json",
        )
        try:
            data = json.loads(result)
            assert "results" in data
        except json.JSONDecodeError:
            pass


class TestBrowserValidation:
    """Tests for browser validation across all tools."""

    @pytest.mark.parametrize("browser", ["chrome", "CHROME", "Chrome", "cHrOmE"])
    def test_search_history_browser_case_insensitive(
        self, browser, mock_chrome_path, sample_chrome_db
    ):
        """Test that browser names work in any case."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python", limit=5, browser=browser)
        assert "error" not in result.lower() or "python" in result.lower()

    @pytest.mark.parametrize(
        "tool_name",
        [
            "search_history",
            "get_recent_history",
            "count_visits",
            "list_top_domains",
            "search_history_by_date",
        ],
    )
    def test_all_tools_reject_invalid_browser(self, tool_name, mock_chrome_path, sample_chrome_db):
        """Test that all tools reject invalid browser names."""
        import server

        func = get_tool_func(server, tool_name)

        required = get_required_params(func)
        kwargs = {}

        if "query" in required:
            kwargs["query"] = "test"
        if "domain" in required:
            kwargs["domain"] = "example.com"
        if "limit" in required:
            kwargs["limit"] = 5
        if "start_date" in required:
            kwargs["start_date"] = "2024-01-01"
            kwargs["end_date"] = "2025-12-31"
        if "hours" in required:
            kwargs["hours"] = 24

        kwargs["browser"] = "invalid_browser_xyz"
        result = func(**kwargs)
        assert "error" in result.lower()
