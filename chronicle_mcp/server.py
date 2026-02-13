"""ChronicleMCP Server - Entry point for MCP protocol.

This module serves as the main entry point for running the MCP server.
All business logic is delegated to the protocol adapter in protocols/mcp.py.

Usage:
    python -m chronicle_mcp.server              # Run in stdio mode
    python -m chronicle_mcp.server dev         # Run with MCP Inspector
    python -m chronicle_mcp.server --help      # Show options
"""

import sys

from chronicle_mcp.protocols.mcp import MCP_TOOLS, get_registered_tools, mcp


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("\nRegistered MCP Tools:")
        for tool_name in get_registered_tools():
            print(f"  - {tool_name}")
    else:
        mcp.run()
