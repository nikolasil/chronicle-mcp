"""MCP protocol adapter for ChronicleMCP.

This module provides the MCP server interface using FastMCP.
All business logic is delegated to the HistoryService in the core layer.
"""

import functools
import json
import logging
import time
import uuid
from collections.abc import Callable
from typing import Any, Literal, TypedDict, TypeVar

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
from chronicle_mcp.core.formatters import format_error_message  # noqa: F401

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

T = TypeVar("T", bound=Callable[..., str])


BrowserType = Literal["chrome", "edge", "firefox", "brave", "safari", "vivaldi", "opera"]
FormatType = Literal["markdown", "json"]
SortOrder = Literal["date", "visit_count", "title"]
MergeStrategy = Literal["latest", "combine", "dedupe"]
KeepStrategy = Literal["most_visits", "most_recent", "first"]
PeriodType = Literal["day", "week", "month"]
EventType = Literal[
    "history_added", "history_deleted", "history_updated",
    "bookmark_added", "bookmark_deleted", "download_added", "download_deleted"
]


class MCPMeta(TypedDict, total=False):
    tool: str
    correlation_id: str | None
    execution_ms: int | None
    browser: str | None
    result_count: int | None
    truncated: bool | None
    sanitized: bool | None
    sanitized_params: list[str] | None


class MCPError(TypedDict, total=False):
    code: str
    message: str
    field: str | None
    valid_options: list[str] | None
    suggestion: str | None
    correlation_id: str | None


class MCPResponse(TypedDict, total=False):
    success: bool
    data: dict | list | str | None
    meta: MCPMeta | None
    error: MCPError | None


class SearchHistoryResult(TypedDict):
    results: list[tuple[str, str, int]]
    count: int
    query: str
    message: str


class RecentHistoryResult(TypedDict):
    results: list[tuple[str, str, int]]
    count: int
    hours: int
    message: str


class CountVisitsResult(TypedDict):
    domain: str
    browser: str
    count: int
    message: str


class TopDomainsResult(TypedDict):
    domains: list[tuple[str, int]]
    count: int
    message: str


class MostVisitedPagesResult(TypedDict):
    pages: list[tuple[str, str, int]]
    count: int
    message: str


class SearchByDateResult(TypedDict):
    results: list[tuple[str, str, int]]
    count: int
    query: str
    start_date: str
    end_date: str
    message: str


class AdvancedSearchResult(TypedDict):
    results: list[tuple[str, str, int]]
    count: int
    query: str
    options: dict[str, Any]
    message: str


class BrowserStatsResult(TypedDict):
    stats: dict[str, Any]
    message: str


class BookmarksResult(TypedDict):
    results: list[tuple[str, str]]
    count: int
    browser: str
    message: str


class DownloadsResult(TypedDict):
    results: list[tuple[str, str, int]]
    count: int
    browser: str
    message: str


class DeleteHistoryResult(TypedDict):
    preview: bool | None
    deleted: int | None
    query: str
    count: int
    browser: str
    message: str


class ExportHistoryResult(TypedDict):
    format: str
    content: str


class SyncHistoryResult(TypedDict):
    dry_run: bool
    source: str
    target: str
    entries_count: int
    merge_strategy: str
    message: str


class BrowserListResult(TypedDict):
    browsers: list[str]
    message: str


def get_error_code(error: Exception) -> str:
    """Get the error code string for an exception."""
    if isinstance(error, ValidationError):
        return "VALIDATION_ERROR"
    elif isinstance(error, BrowserNotFoundError):
        return "BROWSER_NOT_FOUND"
    elif isinstance(error, DatabaseLockedError):
        return "DATABASE_LOCKED"
    elif isinstance(error, PermissionDeniedError):
        return "PERMISSION_DENIED"
    elif isinstance(error, DatabaseError):
        return "DATABASE_ERROR"
    elif isinstance(error, ServiceError):
        return "SERVICE_ERROR"
    else:
        return "INTERNAL_ERROR"


def get_error_suggestion(error: Exception) -> str | None:
    """Get a recovery suggestion for an error."""
    if isinstance(error, ValidationError):
        field = error.field or "input"
        suggestions = {
            "browser": "Use list_available_browsers() to see which browsers are available on this system.",
            "query": "Try a more specific search term. Avoid single characters as they match too many results.",
            "limit": "The limit must be between 1 and the maximum allowed for this operation.",
            "hours": "Hours must be a positive number up to 8760 (one year).",
            "start_date": "Use ISO format (YYYY-MM-DD) for dates.",
            "end_date": "Use ISO format (YYYY-MM-DD) for dates.",
            "fuzzy_threshold": "Threshold must be between 0.0 and 1.0.",
        }
        return suggestions.get(field)
    elif isinstance(error, BrowserNotFoundError):
        return "Use list_available_browsers() to see detected browsers. Make sure you've used the browser and visited some websites."
    elif isinstance(error, DatabaseLockedError):
        return "Close the browser or wait a moment and try again. Browser databases are locked when the browser is running."
    elif isinstance(error, PermissionDeniedError):
        return "Check that your user has permission to access browser data directories."
    return None


def handle_service_error(error: Exception, correlation_id: str | None = None) -> str:
    """Convert service exceptions to structured MCP error responses.

    Args:
        error: Exception from service layer
        correlation_id: Optional ID for debugging

    Returns:
        JSON string with structured error information
    """
    error_code = get_error_code(error)
    suggestion = get_error_suggestion(error)

    error_dict: MCPError = {
        "code": error_code,
        "message": error.message if hasattr(error, "message") else str(error),
        "suggestion": suggestion,
        "correlation_id": correlation_id,
    }

    if isinstance(error, ValidationError):
        error_dict["field"] = error.field
    elif isinstance(error, BrowserNotFoundError):
        error_dict["field"] = "browser"
        if hasattr(error, "browser"):
            error_dict["valid_options"] = [error.browser]

    return json.dumps({
        "success": False,
        "data": None,
        "meta": {"correlation_id": correlation_id} if correlation_id else None,
        "error": error_dict,
    })


def mcp_tool(func: T) -> T:
    """Decorator to register MCP tools with standardized error handling and response wrapping.

    This decorator wraps MCP tools with:
    - Consistent error handling with structured error responses
    - Response metadata (correlation ID, execution time)
    - Standardized response envelope
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        correlation_id = str(uuid.uuid4())[:8]
        start_time = time.monotonic()
        try:
            result = func(*args, **kwargs)
            execution_ms = int((time.monotonic() - start_time) * 1000)

            meta: MCPMeta = {
                "tool": func.__name__,
                "correlation_id": correlation_id,
                "execution_ms": execution_ms,
            }

            if isinstance(result, dict):
                response: MCPResponse = {
                    "success": True,
                    "data": result.get("results") or result.get("data") or result,
                    "meta": meta,
                    "error": None,
                }
                if "count" in result:
                    meta["result_count"] = result["count"]
                if "browser" in result:
                    meta["browser"] = result["browser"]
                if "query" in result:
                    meta["query"] = result["query"]
            else:
                response = {
                    "success": True,
                    "data": result,
                    "meta": meta,
                    "error": None,
                }

            return json.dumps(response, ensure_ascii=False)

        except Exception as e:
            return handle_service_error(e, correlation_id)

    mcp.tool()(wrapper)
    return wrapper  # type: ignore[return-value]


@mcp_tool
def list_available_browsers() -> str:
    """Returns a list of browsers with detected history databases on this system.

    Returns:
        List of available browsers (chrome, edge, firefox)
    """
    result = HistoryService.list_available_browsers()
    return result  # type: ignore[return-value]  # type: ignore[return-value]


@mcp_tool
def search_history(
    query: str,
    limit: int = 5,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Search browser history by keyword to find specific pages visited.

    Use this tool when the user wants to find pages matching a specific topic,
    keyword in title, or substring in URL.

    Distinguishes from similar tools:
    - search_history_by_date: Use when date range is needed
    - search_history_advanced: Use when regex, fuzzy, or domain exclusion needed
    - search_by_domain: Use when searching within a specific domain
    - get_recent_history: Use when looking at recent activity without specific query

    Query examples:
        - "python tutorial" -> pages with both words in title/URL
        - "github.com/api" -> pages from GitHub containing /api
        - "stackoverflow question" -> Stack Overflow pages

    Args:
        query: Keywords to search (case-insensitive partial match).
            Avoid single characters ("a") as they match too many results.
        limit: Maximum number of results to return (1-100, default: 5)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.search_history(
        query=query, limit=limit, browser=browser, format_type=format_type
    )
    return result  # type: ignore[return-value]


@mcp_tool
def get_recent_history(
    hours: int = 24,
    limit: int = 20,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Get recent browsing history from the last N hours.

    Use this tool to see what pages were visited recently without a specific search query.
    Good for "what have I been browsing lately" or checking recent activity.

    Distinguishes from similar tools:
    - search_history: Use when you have a specific keyword to search for
    - search_history_by_date: Use when you need a specific date range (not just "last N hours")
    - list_top_domains: Use when you want aggregated domain stats, not individual visits

    Args:
        hours: Number of hours to look back (1-8760, default: 24). Use 1 for last hour, 168 for last week.
        limit: Maximum number of results (1-100, default: 20)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.get_recent_history(
        hours=hours, limit=limit, browser=browser, format_type=format_type
    )
    return result  # type: ignore[return-value]


@mcp_tool
def count_visits(domain: str, browser: BrowserType = "chrome") -> str:
    """Count total visits to a specific domain.

    Use this tool to get exact visit counts for a domain, useful for analytics
    on how often the user visits specific sites.

    Args:
        domain: Domain to count (e.g., 'github.com', 'stackoverflow.com').
            Do not include protocol (http/https) or path.
        browser: Browser to search - case insensitive

    Returns:
        JSON envelope with success status, data with domain visit count
    """
    result = HistoryService.count_visits(domain=domain, browser=browser)
    return result  # type: ignore[return-value]


@mcp_tool
def list_top_domains(
    limit: int = 10,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Get most visited domains from browser history.

    Use this tool for analytics - see which websites the user visits most.
    Good for productivity analysis and understanding browsing patterns.

    Distinguishes from similar tools:
    - get_most_visited_pages: Shows individual pages, not domains
    - search_history: Use when searching for specific pages
    - get_browser_stats: Shows overall database statistics

    Args:
        limit: Maximum number of domains to return (1-50, default: 10)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.domains list, and metadata
    """
    result = HistoryService.list_top_domains(limit=limit, browser=browser, format_type=format_type)
    return result  # type: ignore[return-value]


@mcp_tool
def search_history_by_date(
    query: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Search browser history within a specific date range.

    Use this tool when the user wants to find pages visited between two dates.
    Good for "what did I browse last week" or researching past activity.

    Distinguishes from similar tools:
    - search_history: Use when you don't need date filtering
    - get_recent_history: Use for "last N hours" without specific dates
    - search_history_advanced: Use when you also need regex/fuzzy/domain exclusion

    Args:
        query: Keywords to search in titles and URLs
        start_date: Start date in ISO format (YYYY-MM-DD), inclusive
        end_date: End date in ISO format (YYYY-MM-DD), inclusive
        limit: Maximum number of results (1-100, default: 10)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.search_history_by_date(
        query=query,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        browser=browser,
        format_type=format_type,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def delete_history(
    query: str,
    limit: int = 100,
    browser: BrowserType = "chrome",
    confirm: bool = False,
) -> str:
    """Delete history entries matching a query.

    DANGER: This permanently deletes browser history. Use confirm=True to actually delete.

    By default (confirm=False), returns a preview of how many entries would be deleted
    without actually deleting them.

    Args:
        query: Search term to match for deletion (case-insensitive)
        limit: Maximum number of entries to delete (1-500, default: 100)
        browser: Browser to delete from - case insensitive
        confirm: Must be True to actually delete. False returns preview only.

    Returns:
        JSON envelope with success status, preview/delete count in data
    """
    result = HistoryService.delete_history(
        query=query, limit=limit, browser=browser, confirm=confirm
    )
    return result  # type: ignore[return-value]


@mcp_tool
def search_by_domain(
    domain: str,
    query: str | None = None,
    limit: int = 20,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
    exclude_domains: list[str] | None = None,
) -> str:
    """Search browser history within a specific domain.

    Use this tool to find pages from a particular website. Good for researching
    activity on specific sites like GitHub, documentation sites, or news outlets.

    Distinguishes from similar tools:
    - search_history: Searches all domains
    - search_history_by_date: Use when you need date filtering too
    - search_history_advanced: Use when you also need regex/fuzzy/exclusion options

    Args:
        domain: Domain to search within (e.g., 'github.com', 'docs.python.org').
            Do not include protocol or path.
        query: Optional search term to filter within the domain
        limit: Maximum number of results (1-100, default: 20)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data
        exclude_domains: List of domains to exclude from results

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.search_by_domain(
        domain=domain,
        query=query,
        limit=limit,
        browser=browser,
        format_type=format_type,
        exclude_domains=exclude_domains,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def get_browser_stats(browser: BrowserType = "chrome") -> str:
    """Get browsing statistics for a browser database.

    Use this tool to get an overview of the browser's history database:
    total entries, unique URLs, date range, and visit counts.

    Args:
        browser: Browser to get stats for - case insensitive

    Returns:
        JSON envelope with success status, data.stats object, and metadata
    """
    result = HistoryService.get_browser_stats(browser=browser)
    return result  # type: ignore[return-value]


@mcp_tool
def get_most_visited_pages(
    limit: int = 20,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Get most visited individual pages from browser history.

    Use this tool for analytics on which specific pages are visited most.
    Good for understanding favorite websites and frequently accessed resources.

    Distinguishes from similar tools:
    - list_top_domains: Shows domains, not individual pages
    - get_browser_stats: Shows overall database stats, not page-level data

    Args:
        limit: Maximum number of pages to return (1-100, default: 20)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.pages list, and metadata
    """
    result = HistoryService.get_most_visited_pages(
        limit=limit, browser=browser, format_type=format_type
    )
    return result  # type: ignore[return-value]


@mcp_tool
def export_history(
    format_type: Literal["csv", "json"] = "csv",
    limit: int = 1000,
    query: str | None = None,
    browser: BrowserType = "chrome",
) -> str:
    """Export browser history to CSV or JSON format.

    Use this tool to export browsing history for backup, analysis, or
    importing into other tools. Exports can be filtered by query.

    Args:
        format_type: Export format - "csv" or "json" (default: csv)
        limit: Maximum entries to export (1-10000, default: 1000)
        query: Optional search filter to only export matching entries
        browser: Browser to export from - case insensitive

    Returns:
        JSON envelope with success status, data.content (exported data), and metadata
    """
    result = HistoryService.export_history(
        format_type=format_type, limit=limit, query=query, browser=browser
    )
    return result  # type: ignore[return-value]


@mcp_tool
def search_history_advanced(
    query: str,
    limit: int = 20,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
    exclude_domains: list[str] | None = None,
    sort_by: SortOrder = "date",
    use_regex: bool = False,
    use_fuzzy: bool = False,
    fuzzy_threshold: float = 0.6,
) -> str:
    """Advanced search with regex, fuzzy matching, and domain exclusion.

    Use this tool when simple keyword search isn't enough. Supports:
    - Regex patterns for complex matching
    - Fuzzy matching for typo tolerance
    - Domain exclusion to filter out unwanted sites
    - Sorting by date, visit count, or title

    Distinguishes from similar tools:
    - search_history: Simple keyword search only
    - search_history_by_date: Date range without regex/fuzzy options
    - search_by_domain: Only searches within specific domain(s)

    Note: Cannot use both use_regex and use_fuzzy simultaneously.

    Args:
        query: Keywords to search, or regex pattern if use_regex=True
        limit: Maximum number of results (1-100, default: 20)
        browser: Browser to search - case insensitive
        format_type: "markdown" for readable text, "json" for structured data
        exclude_domains: List of domains to exclude from results
        sort_by: How to sort results - "date" (default), "visit_count", or "title"
        use_regex: Treat query as regex pattern (default: False)
        use_fuzzy: Enable fuzzy matching for typo tolerance (default: False)
        fuzzy_threshold: Similarity threshold for fuzzy matching (0.0-1.0, default: 0.6)

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
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
    return result  # type: ignore[return-value]


@mcp_tool
def sync_history(
    source_browser: BrowserType,
    target_browser: BrowserType,
    merge_strategy: MergeStrategy = "latest",
    dry_run: bool = True,
) -> str:
    """Sync/copy browser history between browsers.

    Use this tool to migrate history from one browser to another.
    By default (dry_run=True), shows what would be done without making changes.

    Distinguishes from similar tools:
    - export_history: Export to file, not to another browser
    - delete_history: Removes entries, doesn't copy

    Args:
        source_browser: Browser to copy history FROM
        target_browser: Browser to copy history TO
        merge_strategy: How to handle duplicates:
            - "latest": Keep most recently visited (default)
            - "combine": Keep all visits from both
            - "dedupe": Remove exact duplicates
        dry_run: If True, preview changes without applying them (default: True)

    Returns:
        JSON envelope with success status, data about sync operation, and metadata
    """
    result = HistoryService.sync_history(
        source_browser=source_browser,
        target_browser=target_browser,
        merge_strategy=merge_strategy,
        dry_run=dry_run,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def list_available_bookmarks() -> str:
    """List browsers with detected bookmarks on this system.

    Use this to check which browsers have bookmark databases available.
    Not all browsers support bookmark retrieval.

    Returns:
        JSON envelope with success status, list of browsers with bookmarks
    """
    result = HistoryService.list_available_bookmarks()
    return result  # type: ignore[return-value]


@mcp_tool
def list_available_downloads() -> str:
    """List browsers with detected downloads history on this system.

    Use this to check which browsers have download records available.
    Not all browsers track downloads.

    Returns:
        JSON envelope with success status, list of browsers with downloads
    """
    result = HistoryService.list_available_downloads()
    return result  # type: ignore[return-value]


@mcp_tool
def get_bookmarks(
    query: str | None = None,
    limit: int = 50,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Get bookmarks from a browser.

    Use this tool to retrieve saved bookmarks, optionally filtered by search query.

    Distinguishes from similar tools:
    - get_downloads: Shows download history, not bookmarks
    - search_history: Searches visit history, not saved bookmarks

    Args:
        query: Optional search term to filter bookmarks by title or URL
        limit: Maximum number of results (1-100, default: 50)
        browser: Browser to get bookmarks from - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.get_bookmarks(
        query=query,
        limit=limit,
        browser=browser,
        format_type=format_type,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def get_downloads(
    query: str | None = None,
    limit: int = 50,
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Get downloads history from a browser.

    Use this tool to retrieve browser download records, optionally filtered by query.

    Distinguishes from similar tools:
    - get_bookmarks: Shows saved bookmarks, not downloads
    - export_history: Export to file format, not real-time retrieval

    Args:
        query: Optional search term to filter downloads by filename or URL
        limit: Maximum number of results (1-100, default: 50)
        browser: Browser to get downloads from - case insensitive
        format_type: "markdown" for readable text, "json" for structured data

    Returns:
        JSON envelope with success status, data.results list, and metadata
    """
    result = HistoryService.get_downloads(
        query=query,
        limit=limit,
        browser=browser,
        format_type=format_type,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def compare_time_periods(
    start_date1: str,
    end_date1: str,
    start_date2: str,
    end_date2: str,
    browser: BrowserType = "chrome",
) -> str:
    """Compare browsing statistics between two time periods.

    Use this tool for analytics to understand how browsing patterns changed over time.
    Shows changes in total visits, unique URLs, top domains gained/lost, and category breakdown.

    Distinguishes from similar tools:
    - analyze_productivity: Analyzes single period productivity
    - generate_insights_report: Comprehensive single-period report

    Args:
        start_date1: Start date of first period in ISO format (YYYY-MM-DD)
        end_date1: End date of first period in ISO format (YYYY-MM-DD)
        start_date2: Start date of second period in ISO format (YYYY-MM-DD)
        end_date2: End date of second period in ISO format (YYYY-MM-DD)
        browser: Browser to analyze - case insensitive

    Returns:
        JSON envelope with success status, data.period1/period2/changes, and metadata
    """
    result = HistoryService.compare_time_periods(
        start_date1=start_date1,
        end_date1=end_date1,
        start_date2=start_date2,
        end_date2=end_date2,
        browser=browser,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def analyze_productivity(
    start_date: str | None = None,
    end_date: str | None = None,
    browser: BrowserType = "chrome",
) -> str:
    """Analyze browsing productivity and generate recommendations.

    Use this tool to understand how productively time is spent browsing.
    Returns a productivity score (0-100), grade (A-F), category breakdown,
    and actionable recommendations for improvement.

    Distinguishes from similar tools:
    - get_browser_stats: Overview stats, not productivity analysis
    - compare_time_periods: Compares two periods, doesn't score productivity
    - generate_insights_report: Broader report including productivity

    Args:
        start_date: Optional start date in ISO format (YYYY-MM-DD). Defaults to last 7 days.
        end_date: Optional end date in ISO format (YYYY-MM-DD). Defaults to today.
        browser: Browser to analyze - case insensitive

    Returns:
        JSON envelope with success status, data.productivity_score/grade/category_breakdown/recommendations, and metadata
    """
    result = HistoryService.analyze_productivity(
        start_date=start_date,
        end_date=end_date,
        browser=browser,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def suggest_categories(
    browser: BrowserType = "chrome",
    limit: int = 20,
) -> str:
    """Suggest categories for uncategorized URLs in browsing history.

    Use this tool to help organize browsing history by suggesting categories
    (work, news, social, entertainment, etc.) for URLs that haven't been categorized.

    Args:
        browser: Browser to analyze - case insensitive
        limit: Maximum number of suggestions (1-100, default: 20)

    Returns:
        JSON envelope with success status, data.uncategorized list, and metadata
    """
    result = HistoryService.suggest_categories(
        browser=browser,
        limit=limit,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def export_visualization(
    format_type: Literal["chart_json", "csv"] = "chart_json",
    period: PeriodType = "month",
    browser: BrowserType = "chrome",
) -> str:
    """Export browsing data formatted for visualization (Chart.js compatible).

    Use this tool to get ready-to-chart data for dashboards or reports.
    Returns structured data suitable for bar charts, line charts, and pie charts.

    Distinguishes from similar tools:
    - export_history: Raw history export, not chart-ready
    - generate_insights_report: Text/markdown report, not chart data

    Args:
        format_type: "chart_json" for visualization data (default), "csv" for spreadsheet
        period: Time period - "day", "week", or "month" (default: "month")
        browser: Browser to export from - case insensitive

    Returns:
        JSON envelope with success status, data.charts/category_breakdown, and metadata
    """
    result = HistoryService.export_visualization(
        format_type=format_type,
        period=period,
        browser=browser,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def generate_insights_report(
    period: PeriodType = "week",
    browser: BrowserType = "chrome",
    format_type: FormatType = "markdown",
) -> str:
    """Generate comprehensive browsing insights report.

    Use this tool for a complete overview of browsing activity including:
    - Statistics (total entries, visits, date range)
    - Productivity analysis and score
    - Top domains and pages
    - Category breakdown
    - Recommendations

    Distinguishes from similar tools:
    - get_browser_stats: Just database statistics, not insights
    - analyze_productivity: Just productivity analysis, not full report
    - export_visualization: Chart data, not comprehensive report

    Args:
        period: Time period - "day", "week", or "month" (default: "week")
        browser: Browser to analyze - case insensitive
        format_type: "markdown" for readable text (default), "json" for structured data

    Returns:
        JSON envelope with success status, data with comprehensive insights, and metadata
    """
    result = HistoryService.generate_insights_report(
        period=period,
        browser=browser,
        format_type=format_type,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def subscribe_to_history(
    browser: BrowserType = "chrome",
    event_types: list[EventType] | None = None,
) -> str:
    """Subscribe to real-time history changes for a browser.

    Use this tool to receive notifications when browser history changes.
    Returns a subscription_id needed to receive events or unsubscribe.

    Distinguishes from similar tools:
    - get_subscription_status: Check subscription status without subscribing
    - unsubscribe_from_history: Cancel an existing subscription

    Event types available:
    - history_added: New history entry created
    - history_deleted: History entry deleted
    - history_updated: History entry modified
    - bookmark_added: New bookmark added
    - bookmark_deleted: Bookmark removed
    - download_added: New download recorded
    - download_deleted: Download record removed

    Args:
        browser: Browser to subscribe to - case insensitive
        event_types: List of event types to receive. If None, receives history_added and history_deleted.

    Returns:
        JSON envelope with success status, data.subscription_id, and metadata
    """
    if event_types is None:
        event_types = ["history_added", "history_deleted"]

    result = HistoryService.subscribe_history_changes(
        browser=browser,
        event_types=list(event_types),  # type: ignore[arg-type]
        callback=None,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def unsubscribe_from_history(subscription_id: str) -> str:
    """Unsubscribe from history change notifications.

    Use this tool to cancel a previously created subscription and stop
    receiving real-time history change events.

    Args:
        subscription_id: The subscription ID returned from subscribe_to_history

    Returns:
        JSON envelope with success status, data about the unsubscription, and metadata
    """
    result = HistoryService.unsubscribe_history_changes(subscription_id)
    return result  # type: ignore[return-value]


@mcp_tool
def get_subscription_status(subscription_id: str | None = None) -> str:
    """Get subscription status or global event statistics.

    Use this tool to check the status of a specific subscription or see
    overall event statistics for all subscriptions.

    Args:
        subscription_id: Optional specific subscription ID. If None, returns global stats.

    Returns:
        JSON envelope with success status, data about subscription/event stats, and metadata
    """
    result = HistoryService.get_subscription_status(subscription_id)
    return result  # type: ignore[return-value]


@mcp_tool
def find_duplicate_history(
    browser: BrowserType = "chrome",
    similarity_threshold: float = 0.9,
    limit: int = 100,
) -> str:
    """Find potential duplicate history entries based on URL similarity.

    Use this tool to identify duplicate or near-duplicate entries in browsing history,
    which can help clean up cluttered history or reduce storage.

    Distinguishes from similar tools:
    - delete_duplicate_history: Actually removes duplicates (requires confirm=True)
    - delete_history: Deletes based on search query, not similarity

    Args:
        browser: Browser to analyze - case insensitive
        similarity_threshold: URL similarity threshold (0.0-1.0, default: 0.9).
            Higher values = more strict matching (only very similar URLs).
            Lower values = more loose matching (catches more variations).
        limit: Maximum number of duplicate groups to return (1-1000, default: 100)

    Returns:
        JSON envelope with success status, data.duplicate_groups list, and metadata
    """
    result = HistoryService.find_duplicate_entries(
        browser=browser,
        similarity_threshold=similarity_threshold,
        limit=limit,
    )
    return result  # type: ignore[return-value]


@mcp_tool
def delete_duplicate_history(
    browser: BrowserType = "chrome",
    similarity_threshold: float = 0.9,
    keep_strategy: KeepStrategy = "most_visits",
    confirm: bool = False,
) -> str:
    """Delete duplicate history entries.

    DANGER: This permanently deletes duplicate history entries. Use confirm=True to actually delete.

    By default (confirm=False), returns a preview of how many entries would be deleted
    without actually deleting them.

    Distinguishes from similar tools:
    - find_duplicate_history: Just identifies duplicates, doesn't delete
    - delete_history: Deletes based on search query, not similarity

    Args:
        browser: Browser to clean - case insensitive
        similarity_threshold: URL similarity threshold (0.0-1.0, default: 0.9).
            Higher values = more strict matching.
        keep_strategy: Which entry to keep - "most_visits" (default), "most_recent", or "first"
        confirm: Must be True to actually delete. False returns preview only.

    Returns:
        JSON envelope with success status, data.preview/delete info, and metadata
    """
    result = HistoryService.delete_duplicates(
        browser=browser,
        similarity_threshold=similarity_threshold,
        keep_strategy=keep_strategy,
        confirm=confirm,
    )
    return result  # type: ignore[return-value]
