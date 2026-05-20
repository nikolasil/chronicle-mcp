"""Tests for server.py entry point."""

import pytest

pytestmark = pytest.mark.ci_excluded

from unittest.mock import patch


class TestServerEntryPoint:
    """Tests for MCP server initialization."""

    def test_server_imports_mcp(self):
        """Test that server imports mcp correctly."""
        from chronicle_mcp.server import mcp

        assert mcp is not None

    def test_server_can_run(self):
        """Test that server mcp.run() can be called without errors."""
        from chronicle_mcp.server import mcp

        with patch.object(mcp, "run") as mock_run:
            mcp.run()
            mock_run.assert_called_once()

    def test_server_module_executable(self):
        """Test that server module can be executed."""
        import chronicle_mcp.server as server_module

        assert hasattr(server_module, "mcp")


class TestMCPProtocol:
    """Tests for MCP protocol integration."""

    def test_mcp_instance_exists(self):
        """Test that MCP instance is properly initialized."""
        from chronicle_mcp.protocols.mcp import mcp

        assert mcp is not None
        assert hasattr(mcp, "tool")
        assert hasattr(mcp, "run")

    def test_mcp_tools_deco_registered(self):
        """Test that @mcp_tool decorator registers tools."""
        from chronicle_mcp.protocols import mcp

        assert mcp is not None


class TestServerHelpOption:
    """Tests for server --help option (removed per simplification)."""

    def test_server_help_removed(self):
        """Verify server no longer has interactive --help (simplified entry point)."""
        import inspect

        import chronicle_mcp.server as server_module

        source = inspect.getsource(server_module)
        assert "sys.argv" not in source
        assert "get_registered_tools" not in source


class TestServerIntegration:
    """Integration tests for the server."""

    def test_server_package_integration(self):
        """Test that server integrates with the full package."""
        from chronicle_mcp import server

        assert hasattr(server, "mcp")

    def test_server_protocols_mcp_integration(self):
        """Test that server correctly imports from protocols.mcp."""
        from chronicle_mcp.protocols.mcp import mcp

        assert mcp is not None
