"""ChronicleMCP Server - Entry point for MCP protocol.

This module serves as the main entry point for running the MCP server.
All business logic is delegated to the protocol adapter in protocols/mcp.py.

Usage:
    python -m chronicle_mcp.server              # Run in stdio mode
    python -m chronicle_mcp.server dev         # Run with MCP Inspector
    python -m chronicle_mcp.server --help      # Show options
"""

from chronicle_mcp.protocols.mcp import mcp

if __name__ == "__main__":
    mcp.run()
