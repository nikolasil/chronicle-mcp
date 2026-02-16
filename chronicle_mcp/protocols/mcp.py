"""MCP protocol adapter for ChronicleMCP.

This module provides the MCP server interface using FastMCP.
All business logic is delegated to the HistoryService in the core layer.
"""

import logging
from typing import Any, cast

from fastmcp import FastMCP

from chronicle_mcp.config import setup_logging
from chronicle_mcp.core import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    HistoryService,
    PermissionDeniedError,
    ServiceError,
    ValidationError,
)
from chronicle_mcp.core.formatters import format_error_message

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

MCP_TOOLS: list[str] = []


def tool(func: Any) -> Any:
    """Decorator to register MCP tools with error handling."""
    registered = mcp.tool()(func)
    MCP_TOOLS.append(func.__name__)
    return registered


def handle_service_error(error: Exception) -> str:
    """Convert service exceptions to MCP error strings.

    Args:
        error: Exception from service layer

    Returns:
        Formatted error message for MCP response
    """
    if isinstance(error, ValidationError):
        return format_error_message(error.message)
    elif isinstance(error, BrowserNotFoundError):
        return format_error_message(error.message)
    elif isinstance(error, DatabaseLockedError):
        return format_error_message(error.message)
    elif isinstance(error, PermissionDeniedError):
        return format_error_message(error.message)
    elif isinstance(error, DatabaseError):
        return format_error_message(error.message)
    elif isinstance(error, ServiceError):
        return format_error_message(error.message)
    else:
        logger.exception("Unexpected error in MCP tool")
        return format_error_message("An unexpected error occurred")


@tool
def list_available_browsers() -> str:
    """Returns a list of browsers with detected history databases on this system.

    Returns:
        List of available browsers (chrome, edge, firefox)
    """
    try:
        result = HistoryService.list_available_browsers()
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Searches browser history for keywords in titles or URLs.

    Args:
        query: Search term to look for in titles or URLs
        limit: Maximum number of results to return (1-100)
        browser: Browser to search (chrome, edge, firefox) - case insensitive
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of matching history entries or error message
    """
    try:
        result = HistoryService.search_history(
            query=query, limit=limit, browser=browser, format_type=format_type
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def get_recent_history(
    hours: int = 24,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Gets recent browsing history from the last N hours.

    Args:
        hours: Number of hours to look back (default: 24)
        limit: Maximum number of results (1-100, default: 20)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of recent history entries or error message
    """
    try:
        result = HistoryService.get_recent_history(
            hours=hours, limit=limit, browser=browser, format_type=format_type
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def count_visits(domain: str, browser: str = "chrome") -> str:
    """Counts total visits to a specific domain.

    Args:
        domain: Domain to count (e.g., 'github.com', 'stackoverflow.com')
        browser: Browser to search (chrome, edge, firefox)

    Returns:
        Number of visits to the domain or error message
    """
    try:
        result = HistoryService.count_visits(domain=domain, browser=browser)
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def list_top_domains(
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Gets the most visited domains from browser history.

    Args:
        limit: Maximum number of domains to return (1-50, default: 10)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of top domains or error message
    """
    try:
        result = HistoryService.list_top_domains(
            limit=limit, browser=browser, format_type=format_type
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def search_history_by_date(
    query: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Searches browser history within a date range.

    Args:
        query: Search term to look for in titles or URLs
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        limit: Maximum number of results (1-100)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of matching history entries or error message
    """
    try:
        result = HistoryService.search_history_by_date(
            query=query,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            browser=browser,
            format_type=format_type,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def delete_history(
    query: str,
    limit: int = 100,
    browser: str = "chrome",
    confirm: bool = False,
) -> str:
    """Deletes history entries matching a query.

    Args:
        query: Search term to match for deletion
        limit: Maximum number of entries to delete (1-500)
        browser: Browser to search (chrome, edge, firefox)
        confirm: Must be True to actually delete; False returns preview

    Returns:
        Number of entries deleted or preview message
    """
    try:
        result = HistoryService.delete_history(
            query=query, limit=limit, browser=browser, confirm=confirm
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def search_by_domain(
    domain: str,
    query: str | None = None,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
    exclude_domains: list[str] | None = None,
) -> str:
    """Searches history within specific domain(s).

    Args:
        domain: Domain to search within (e.g., 'github.com', 'docs.python.org')
        query: Optional search term within the domain
        limit: Maximum number of results (1-100)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)
        exclude_domains: Domains to exclude from results

    Returns:
        Formatted list of matching history entries or error message
    """
    try:
        result = HistoryService.search_by_domain(
            domain=domain,
            query=query,
            limit=limit,
            browser=browser,
            format_type=format_type,
            exclude_domains=exclude_domains,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def get_browser_stats(browser: str = "chrome") -> str:
    """Gets browsing statistics for the browser database.

    Args:
        browser: Browser to get stats for (chrome, edge, firefox)

    Returns:
        JSON string with browsing statistics
    """
    try:
        result = HistoryService.get_browser_stats(browser=browser)
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def get_most_visited_pages(
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Gets the most visited individual pages.

    Args:
        limit: Maximum number of pages to return (1-100)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of most visited pages or error message
    """
    try:
        result = HistoryService.get_most_visited_pages(
            limit=limit, browser=browser, format_type=format_type
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def export_history(
    format_type: str = "csv",
    limit: int = 1000,
    query: str | None = None,
    browser: str = "chrome",
) -> str:
    """Exports history to CSV or JSON format.

    Args:
        format_type: Export format (csv or json)
        limit: Maximum entries to export (1-10000)
        query: Optional search filter
        browser: Browser to export from (chrome, edge, firefox)

    Returns:
        CSV or JSON formatted history data
    """
    try:
        result = HistoryService.export_history(
            format_type=format_type, limit=limit, query=query, browser=browser
        )
        return cast(str, result["content"])
    except Exception as e:
        return handle_service_error(e)


@tool
def search_history_advanced(
    query: str,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
    exclude_domains: list[str] | None = None,
    sort_by: str = "date",
    use_regex: bool = False,
    use_fuzzy: bool = False,
    fuzzy_threshold: float = 0.6,
) -> str:
    """Advanced search with multiple options.

    Args:
        query: Search term to look for in titles or URLs
        limit: Maximum number of results (1-100)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)
        exclude_domains: Domains to exclude from results
        sort_by: Sort order (date, visit_count, title)
        use_regex: Use regex pattern matching
        use_fuzzy: Use fuzzy matching for typos
        fuzzy_threshold: Minimum similarity score for fuzzy matching (0.0-1.0)

    Returns:
        Formatted list of matching history entries or error message
    """
    try:
        result = HistoryService.search_history_advanced(
            query=query,
            limit=limit,
            browser=browser,
            format_type=format_type,
            exclude_domains=exclude_domains,
            sort_by=sort_by,
            use_regex=use_regex,
            use_fuzzy=use_fuzzy,
            fuzzy_threshold=fuzzy_threshold,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def sync_history(
    source_browser: str,
    target_browser: str,
    merge_strategy: str = "latest",
    dry_run: bool = True,
) -> str:
    """Syncs history between browsers.

    Args:
        source_browser: Browser to copy history from
        target_browser: Browser to copy history to
        merge_strategy: How to handle duplicates (latest, combine, dedupe)
        dry_run: If True, show what would be done without making changes

    Returns:
        Summary of sync operation
    """
    try:
        result = HistoryService.sync_history(
            source_browser=source_browser,
            target_browser=target_browser,
            merge_strategy=merge_strategy,
            dry_run=dry_run,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def list_available_bookmarks() -> str:
    """Returns a list of browsers with detected bookmarks on this system.

    Returns:
        List of available browsers with bookmarks
    """
    try:
        result = HistoryService.list_available_bookmarks()
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def list_available_downloads() -> str:
    """Returns a list of browsers with detected downloads history on this system.

    Returns:
        List of available browsers with downloads
    """
    try:
        result = HistoryService.list_available_downloads()
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def get_bookmarks(
    query: str | None = None,
    limit: int = 50,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Gets bookmarks from a browser.

    Args:
        query: Optional search term to filter bookmarks
        limit: Maximum number of results (1-100)
        browser: Browser to get bookmarks from (chrome, edge, firefox, brave, vivaldi, opera)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of bookmarks or error message
    """
    try:
        result = HistoryService.get_bookmarks(
            query=query,
            limit=limit,
            browser=browser,
            format_type=format_type,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


@tool
def get_downloads(
    query: str | None = None,
    limit: int = 50,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> str:
    """Gets downloads history from a browser.

    Args:
        query: Optional search term to filter downloads
        limit: Maximum number of results (1-100)
        browser: Browser to get downloads from (chrome, edge, firefox, brave, vivaldi, opera)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of downloads or error message
    """
    try:
        result = HistoryService.get_downloads(
            query=query,
            limit=limit,
            browser=browser,
            format_type=format_type,
        )
        return cast(str, result["message"])
    except Exception as e:
        return handle_service_error(e)


def get_registered_tools() -> list[str]:
    """Returns the list of registered MCP tool names."""
    return MCP_TOOLS.copy()
