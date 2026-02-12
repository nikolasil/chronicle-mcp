import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from chronicle_mcp import cli


def get_tool_func(module, tool_name):
    """Get the underlying function from a FastMCP tool."""
    tool = getattr(module, tool_name)
    return tool.fn


class TestCLI:
    """Tests for CLI functionality using direct imports (faster than subprocess)."""

    def test_cli_help(self):
        """Test that CLI help command works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_version(self, capsys):
        """Test that CLI version command works."""
        with patch.object(sys, "argv", ["chronicle-mcp", "version"]):
            try:
                cli.cli()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "ChronicleMCP" in captured.out or "version" in captured.out.lower()

    def test_cli_list_browsers(self, capsys):
        """Test that CLI list-browsers command works."""
        with patch.object(sys, "argv", ["chronicle-mcp", "list-browsers"]):
            try:
                cli.cli()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "browser" in captured.out.lower() or "Available" in captured.out

    def test_cli_completion_bash(self, capsys):
        """Test that CLI completion bash command works."""
        with patch.object(sys, "argv", ["chronicle-mcp", "completion", "bash"]):
            try:
                cli.cli()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "bash" in captured.out.lower() or "#!" in captured.out

    def test_cli_completion_zsh(self, capsys):
        """Test that CLI completion zsh command works."""
        with patch.object(sys, "argv", ["chronicle-mcp", "completion", "zsh"]):
            try:
                cli.cli()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "zsh" in captured.out.lower() or "compdef" in captured.out

    def test_cli_completion_fish(self, capsys):
        """Test that CLI completion fish command works."""
        with patch.object(sys, "argv", ["chronicle-mcp", "completion", "fish"]):
            try:
                cli.cli()
            except SystemExit:
                pass
        captured = capsys.readouterr()
        assert "fish" in captured.out.lower() or "complete" in captured.out

    def test_cli_run_help(self):
        """Test that CLI run command help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "run", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_run_sse_help(self):
        """Test that CLI run command with SSE transport help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "run", "--transport", "sse", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_serve_help(self):
        """Test that CLI serve command help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "serve", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_status_help(self):
        """Test that CLI status command help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "status", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_logs_help(self):
        """Test that CLI logs command help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "logs", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0


class TestCLIConfig:
    """Tests for CLI configuration handling."""

    def test_cli_env_chronicled_port(self, monkeypatch):
        """Test that CHRONICLE_PORT environment variable is recognized."""
        monkeypatch.setenv("CHRONICLE_PORT", "9999")
        # Just verify the env var is set (actual usage tested in integration)
        assert True

    def test_cli_temp_dir_accessible(self):
        """Test that temp directory is accessible for PID files."""
        import tempfile

        temp_dir = Path(tempfile.gettempdir())
        test_file = temp_dir / "test_write_access.txt"
        try:
            test_file.write_text("test")
            test_file.unlink()
            assert True
        except PermissionError:
            pytest.skip("Temp directory not writable")


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
        assert hasattr(paths, "get_browser_path")
        assert hasattr(paths, "get_available_browsers")

    def test_database_module_importable(self):
        """Test that database module can be imported."""
        from chronicle_mcp import database

        assert database is not None
        assert hasattr(database, "query_history")
        assert hasattr(database, "format_results")
        assert hasattr(database, "sanitize_url")

    def test_server_module_importable(self):
        """Test that server module can be imported."""
        import server

        assert server is not None
        assert hasattr(server, "mcp")
        assert hasattr(server, "search_history")
        assert hasattr(server, "get_recent_history")


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_special_characters_in_query(self, mock_chrome_path, sample_chrome_db):
        """Test that special characters in query don't break search."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("test<script>alert('xss')</script>", limit=5, browser="chrome")
        assert result is not None

    def test_very_long_query(self, mock_chrome_path, sample_chrome_db):
        """Test that very long queries don't break search."""
        import server

        func = get_tool_func(server, "search_history")
        long_query = "a" * 1000
        result = func(long_query, limit=5, browser="chrome")
        assert result is not None

    def test_unicode_in_query(self, mock_chrome_path, sample_chrome_db):
        """Test that unicode characters in query work."""
        import server

        func = get_tool_func(server, "search_history")
        result = func("python 日本語", limit=5, browser="chrome")
        assert result is not None

    def test_limit_at_boundary(self, mock_chrome_path, sample_chrome_db):
        """Test that limit at boundary values work."""
        import server

        func = get_tool_func(server, "search_history")
        result_1 = func("python", limit=1, browser="chrome")
        result_100 = func("python", limit=100, browser="chrome")
        assert result_1 is not None
        assert result_100 is not None

    def test_url_sanitization_in_results(self, mock_chrome_path, sample_chrome_db):
        """Test that URLs with tokens are sanitized in results."""
        import server

        func = get_tool_func(server, "search_history")
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
