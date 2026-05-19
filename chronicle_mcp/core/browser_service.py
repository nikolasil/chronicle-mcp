"""Browser availability service for ChronicleMCP.

This module provides functions to detect available browsers, bookmarks,
and downloads databases on the local system.
"""

from typing import Any

from chronicle_mcp.core.formatters import format_available_browsers
from chronicle_mcp.paths import (
    get_available_bookmarks,
    get_available_browsers,
    get_available_downloads,
)


def list_available_browsers() -> dict[str, Any]:
    """Get list of available browsers with detected history databases.

    Returns:
        Dictionary with 'browsers' list and 'message' string
    """
    browsers = get_available_browsers()
    return {"browsers": browsers, "message": format_available_browsers(browsers)}


def list_available_bookmarks() -> dict[str, Any]:
    """Get list of browsers with detected bookmarks databases.

    Returns:
        Dictionary with 'browsers' list and 'message' string
    """
    browsers = get_available_bookmarks()
    return {"browsers": browsers, "message": format_available_browsers(browsers)}


def list_available_downloads() -> dict[str, Any]:
    """Get list of browsers with detected downloads history databases.

    Returns:
        Dictionary with 'browsers' list and 'message' string
    """
    browsers = get_available_downloads()
    return {"browsers": browsers, "message": format_available_browsers(browsers)}
