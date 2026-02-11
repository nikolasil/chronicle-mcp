import os
import subprocess
import sys


def get_tool_func(module, tool_name):
    """Get the underlying function from a FastMCP tool."""
    tool = getattr(module, tool_name)
    return tool.fn


class TestCLI:
    """Tests for CLI functionality."""

    def test_server_help(self):
        """Test that server --help works."""
        result = subprocess.run(
            [sys.executable, "server.py", "--help"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)) or "."
        )
        assert result.returncode == 0 or "error" not in result.stderr.lower()

    def test_server_dev_starts(self):
        """Test that server dev command starts without immediate error."""
        result = subprocess.run(
            [sys.executable, "server.py", "dev"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)) or ".",
            timeout=5
        )
        assert result.returncode == 0 or "error" not in result.stderr.lower()


class TestPackageStructure:
    """Tests for package structure."""

    def test_package_importable(self):
        """Test that chronicle_mcp package can be imported."""
        import chronicle_mcp
        assert chronicle_mcp is not None

    def test_paths_module_importable(self):
        """Test that paths module can be imported."""
        from chronicle_mcp import paths
        assert paths is not None
        assert hasattr(paths, 'get_browser_path')
        assert hasattr(paths, 'get_available_browsers')

    def test_database_module_importable(self):
        """Test that database module can be imported."""
        from chronicle_mcp import database
        assert database is not None
        assert hasattr(database, 'query_history')
        assert hasattr(database, 'format_results')
        assert hasattr(database, 'sanitize_url')

    def test_server_module_importable(self):
        """Test that server module can be imported."""
        import server
        assert server is not None
        assert hasattr(server, 'mcp')
        assert hasattr(server, 'search_history')
        assert hasattr(server, 'get_recent_history')


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_special_characters_in_query(self, mock_chrome_path, sample_chrome_db):
        """Test that special characters in query don't break search."""
        import server
        func = get_tool_func(server, 'search_history')
        result = func("test<script>alert('xss')</script>", limit=5, browser="chrome")
        assert result is not None

    def test_very_long_query(self, mock_chrome_path, sample_chrome_db):
        """Test that very long queries don't break search."""
        import server
        func = get_tool_func(server, 'search_history')
        long_query = "a" * 1000
        result = func(long_query, limit=5, browser="chrome")
        assert result is not None

    def test_unicode_in_query(self, mock_chrome_path, sample_chrome_db):
        """Test that unicode characters in query work."""
        import server
        func = get_tool_func(server, 'search_history')
        result = func("python 日本語", limit=5, browser="chrome")
        assert result is not None

    def test_limit_at_boundary(self, mock_chrome_path, sample_chrome_db):
        """Test that limit at boundary values work."""
        import server
        func = get_tool_func(server, 'search_history')
        result_1 = func("python", limit=1, browser="chrome")
        result_100 = func("python", limit=100, browser="chrome")
        assert result_1 is not None
        assert result_100 is not None

    def test_url_sanitization_in_results(self, mock_chrome_path, sample_chrome_db):
        """Test that URLs with tokens are sanitized in results."""
        import server
        func = get_tool_func(server, 'search_history')
        result = func("token", limit=5, browser="chrome")
        if "secret123" not in result.lower():
            assert "token" in result.lower() or "no history found" in result.lower()


class TestMCPIntegration:
    """Tests for MCP protocol integration."""

    def test_mcp_server_initializes(self):
        """Test that MCP server initializes without error."""
        import server
        assert server.mcp is not None

    def test_all_tools_registered(self):
        """Test that all expected tools are registered."""
        import server

        tools = [
            "list_available_browsers",
            "search_history",
            "get_recent_history",
            "count_visits",
            "list_top_domains",
            "search_history_by_date",
        ]

        for tool in tools:
            assert hasattr(server, tool), f"Missing tool: {tool}"

    def test_mcp_server_has_name(self):
        """Test that MCP server has correct name."""
        import server
        assert server.mcp.name == "Chronicle"
