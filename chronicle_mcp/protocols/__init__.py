"""Protocol adapters for ChronicleMCP.

This package contains thin protocol adapters that delegate all
business logic to the HistoryService in the core layer.
"""

from chronicle_mcp.protocols.http import app, run_http_server
from chronicle_mcp.protocols.mcp import (
    MCP_TOOLS,
    get_registered_tools,
    mcp,
)

__all__ = [
    "mcp",
    "app",
    "run_http_server",
    "MCP_TOOLS",
    "get_registered_tools",
]
