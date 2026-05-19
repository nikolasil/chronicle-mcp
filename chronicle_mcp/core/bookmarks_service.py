from typing import Any

from chronicle_mcp.core.exceptions import BrowserNotFoundError
from chronicle_mcp.core.formatters import format_bookmarks, format_downloads
from chronicle_mcp.core.validation import validate_browser, validate_format_type, validate_limit
from chronicle_mcp.database import query_bookmarks, query_downloads
from chronicle_mcp.paths import get_bookmark_path, get_browser_schema, get_download_path


def get_bookmarks(
    query: str | None = None,
    limit: int = 50,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Get bookmarks from a browser.

    Args:
        query: Optional search term to filter bookmarks
        limit: Maximum results (1-100)
        browser: Browser to get bookmarks from
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with bookmarks and formatted message
    """
    browser_lower = validate_browser(browser)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    bookmark_path = get_bookmark_path(browser_lower)
    if not bookmark_path:
        raise BrowserNotFoundError(f"{browser_lower} (bookmarks not found)")

    schema = get_browser_schema(browser_lower)
    bookmarks = query_bookmarks(bookmark_path, schema, query, limit_val)

    return {
        "results": bookmarks,
        "count": len(bookmarks),
        "browser": browser_lower,
        "message": format_bookmarks(bookmarks, format_clean),
    }


def get_downloads(
    query: str | None = None,
    limit: int = 50,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Get downloads history from a browser.

    Args:
        query: Optional search term to filter downloads
        limit: Maximum results (1-100)
        browser: Browser to get downloads from
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with downloads and formatted message
    """
    browser_lower = validate_browser(browser)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    download_path = get_download_path(browser_lower)
    if not download_path:
        raise BrowserNotFoundError(f"{browser_lower} (downloads not found)")

    schema = get_browser_schema(browser_lower)
    downloads = query_downloads(download_path, schema, query, limit_val)

    return {
        "results": downloads,
        "count": len(downloads),
        "browser": browser_lower,
        "message": format_downloads(downloads, format_clean),
    }
