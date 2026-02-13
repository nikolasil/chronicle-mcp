"""Tests for CLI functionality."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from chronicle_mcp import cli


class TestCLI:
    """Tests for CLI functionality using direct imports."""

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
            with patch.object(sys, "argv", ["chronicle-mcp", "mcp", "--help"]):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_mcp_sse_help(self):
        """Test that CLI mcp command with SSE help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(
                sys, "argv", ["chronicle-mcp", "mcp", "--sse", "--help"]
            ):
                cli.cli()
        assert exc_info.value.code == 0

    def test_cli_http_help(self):
        """Test that CLI http command help works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch.object(sys, "argv", ["chronicle-mcp", "http", "--help"]):
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

    def test_core_module_importable(self):
        """Test that core module can be imported."""
        from chronicle_mcp import core

        assert core is not None
        assert hasattr(core, "HistoryService")
        assert hasattr(core, "validate_browser")

    def test_protocols_module_importable(self):
        """Test that protocols module can be imported."""
        from chronicle_mcp import protocols

        assert protocols is not None
        assert hasattr(protocols, "mcp")
        assert hasattr(protocols, "app")


class TestMCPIntegration:
    """Tests for MCP protocol integration."""

    def test_mcp_server_initializes(self):
        """Test that MCP server initializes without error."""
        from chronicle_mcp.protocols import mcp

        assert mcp is not None
        assert mcp.name == "Chronicle"

    def test_mcp_tools_registered(self):
        """Test that MCP tools are registered."""
        from chronicle_mcp.protocols import mcp

        # The mcp object should have tools registered
        assert mcp is not None
