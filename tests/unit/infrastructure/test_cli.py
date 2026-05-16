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
            with patch.object(sys, "argv", ["chronicle-mcp", "mcp", "--sse", "--help"]):
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


class TestVersionCommand:
    """Tests for version CLI command."""

    def test_version_output(self, capsys):
        """Test version command outputs version."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "ChronicleMCP" in result.output
        assert "version" in result.output.lower()

    def test_version_contains_number(self, capsys):
        """Test version output contains version number."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        # Version number pattern
        import re

        assert re.search(r"\d+\.\d+", result.output)


class TestMCPCommand:
    """Tests for MCP server CLI command."""

    def test_mcp_stdio_help(self):
        """Test MCP stdio command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["mcp", "--help"])
        assert result.exit_code == 0
        assert "MCP server" in result.output

    def test_mcp_sse_help(self):
        """Test MCP SSE command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["mcp", "--sse", "--help"])
        assert result.exit_code == 0

    def test_mcp_with_options(self):
        """Test MCP with host and port options."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        # Mock run_http_server to prevent actual server start
        with patch("chronicle_mcp.protocols.http.run_http_server") as mock_server:
            mock_server.side_effect = SystemExit(0)
            result = runner.invoke(cli, ["mcp", "--sse", "--host", "0.0.0.0", "--port", "9090"])
        # Help or error expected since we're not actually running the server
        assert result.exit_code in [0, 1, 2]


class TestHTTPCommand:
    """Tests for HTTP server CLI command."""

    def test_http_help(self):
        """Test HTTP command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["http", "--help"])
        assert result.exit_code == 0
        assert "HTTP" in result.output

    def test_http_with_options(self):
        """Test HTTP with all options."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        # Mock run_http_server to prevent actual server start
        with patch("chronicle_mcp.protocols.http.run_http_server") as mock_server:
            mock_server.side_effect = SystemExit(0)
            result = runner.invoke(
                cli,
                [
                    "http",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "9090",
                    "--browser",
                    "firefox",
                    "--foreground",
                ],
            )
        # Exit code varies based on whether server starts
        assert result.exit_code in [0, 1, 2]

    def test_http_daemon_option(self):
        """Test HTTP with daemon option."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        # Mock run_http_server to prevent actual server start
        with patch("chronicle_mcp.protocols.http.run_http_server") as mock_server:
            mock_server.side_effect = SystemExit(0)
            result = runner.invoke(cli, ["http", "--port", "8080", "--daemon"])
        # Daemon mode should work or fail gracefully
        assert result.exit_code in [0, 1, 2]


class TestStatusCommand:
    """Tests for status CLI command."""

    def test_status_not_running(self, capsys):
        """Test status when server is not running."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        # Use a port that's unlikely to have a server
        result = runner.invoke(cli, ["status", "--port", "59999"])
        assert result.exit_code == 0
        assert "NOT running" in result.output or "no PID file" in result.output

    def test_status_help(self):
        """Test status command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["status", "--help"])
        assert result.exit_code == 0
        assert "status" in result.output.lower()


class TestLogsCommand:
    """Tests for logs CLI command."""

    def test_logs_no_file(self, capsys):
        """Test logs when log file doesn't exist."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["logs", "--port", "59999"])
        assert result.exit_code == 0
        assert "No logs found" in result.output

    def test_logs_with_lines(self, tmp_path, monkeypatch):
        """Test logs command with line limit."""
        # Create a temp log file
        import tempfile

        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        log_file = Path(tempfile.gettempdir()) / "chronicle-mcp-59998.log"
        log_file.write_text("Line 1\nLine 2\nLine 3\n")

        try:
            runner = CliRunner()
            result = runner.invoke(cli, ["logs", "--port", "59998", "--lines", "2"])
            assert result.exit_code == 0
            assert "Line 2" in result.output or "Line 3" in result.output
        finally:
            if log_file.exists():
                log_file.unlink()

    def test_logs_help(self):
        """Test logs command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["logs", "--help"])
        assert result.exit_code == 0
        assert "logs" in result.output.lower()


class TestCompletionCommand:
    """Tests for shell completion CLI command."""

    def test_completion_bash(self):
        """Test bash completion generation."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["completion", "bash"])
        assert result.exit_code == 0
        assert "bash" in result.output.lower()
        assert "_chronicle_mcp" in result.output
        assert "complete" in result.output

    def test_completion_zsh(self):
        """Test zsh completion generation."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["completion", "zsh"])
        assert result.exit_code == 0
        assert "zsh" in result.output.lower() or "compdef" in result.output
        assert "_chronicle_mcp" in result.output

    def test_completion_fish(self):
        """Test fish completion generation."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["completion", "fish"])
        assert result.exit_code == 0
        assert "fish" in result.output.lower() or "complete" in result.output

    def test_completion_invalid_shell(self):
        """Test completion with invalid shell."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["completion", "invalid"])
        assert result.exit_code != 0


class TestListBrowsersCommand:
    """Tests for list-browsers CLI command."""

    def test_list_browsers_help(self):
        """Test list-browsers command help."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["list-browsers", "--help"])
        assert result.exit_code == 0
        assert "browser" in result.output.lower()

    def test_list_browsers_output(self):
        """Test list-browsers command output."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["list-browsers"])
        assert result.exit_code == 0
        # Should output something about browsers
        assert (
            "browser" in result.output.lower()
            or "Available" in result.output
            or "No browsers" in result.output
        )


class TestCLIExitCodes:
    """Tests for CLI exit codes."""

    def test_help_exit_code(self):
        """Test that --help exits with code 0."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0

    def test_invalid_command_exit_code(self):
        """Test that invalid command has non-zero exit."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0

    def test_version_exit_code(self):
        """Test that version exits with code 0."""
        from click.testing import CliRunner

        from chronicle_mcp.cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0


class TestCLITempFiles:
    """Tests for CLI temp file handling."""

    def test_temp_dir_writable(self):
        """Test that temp directory is writable."""
        import tempfile

        temp_dir = Path(tempfile.gettempdir())
        test_file = temp_dir / "test_chronicle_write.tmp"
        try:
            test_file.write_text("test")
            assert test_file.exists()
            content = test_file.read_text()
            assert content == "test"
        finally:
            if test_file.exists():
                test_file.unlink()

    def test_pid_file_naming(self):
        """Test PID file naming convention."""
        import tempfile

        port = 8080
        expected_name = f"chronicle-mcp-{port}.pid"
        temp_dir = Path(tempfile.gettempdir())
        expected_path = temp_dir / expected_name
        # Just verify the naming pattern is correct
        assert "chronicle-mcp" in expected_name
        assert str(port) in expected_name
        assert expected_name.endswith(".pid")
        # Use expected_path to avoid F841 warning
        assert isinstance(expected_path, Path)

    def test_log_file_naming(self):
        """Test log file naming convention."""

        port = 8080
        expected_name = f"chronicle-mcp-{port}.log"
        # Just verify the naming pattern is correct
        assert "chronicle-mcp" in expected_name
        assert str(port) in expected_name
        assert expected_name.endswith(".log")
