"""ChronicleMCP Server - Model Context Protocol server for browser history.

This module provides MCP tools for searching and querying local browser history
across Chrome, Firefox, and Edge browsers.

Usage:
    python server.py              # Run in stdio mode (default for AI agents)
    python server.py dev         # Run with MCP Inspector
    python server.py --help      # Show options
"""

import logging
import sqlite3
from typing import Any

from fastmcp import FastMCP

from chronicle_mcp.config import setup_logging
from chronicle_mcp.connection import ConnectionError, get_history_connection
from chronicle_mcp.database import (
    count_domain_visits as db_count_visits,
)
from chronicle_mcp.database import (
    export_history as db_export_history,
)
from chronicle_mcp.database import (
    format_results,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import (
    get_top_domains as db_get_top_domains,
)
from chronicle_mcp.database import (
    search_by_date as db_search_by_date,
)
from chronicle_mcp.paths import get_available_browsers, get_browser_path

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

VALID_BROWSERS = ["chrome", "edge", "firefox", "brave", "safari", "vivaldi", "opera"]

MCP_TOOLS = []


def tool(func: Any) -> Any:
    """Decorator to register MCP tools with error handling."""
    registered = mcp.tool()(func)
    MCP_TOOLS.append(func.__name__)
    return registered


@tool
def list_available_browsers() -> str:
    """Returns a list of browsers with detected history databases on this system.

    Returns:
        List of available browsers (chrome, edge, firefox)
    """
    available = get_available_browsers()
    if not available:
        return "No browsers with history found on this system"
    return f"Available browsers: {', '.join(available)}"


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
    browser_lower = browser.lower()

    if not query or not query.strip():
        logger.warning("Empty query received")
        return "Error: Query cannot be empty"

    if not isinstance(limit, int):
        return "Error: Limit must be an integer"
    if limit < 1 or limit > 100:
        return "Error: Limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    logger.info(f"Searching history for '{query}' in {browser_lower} (limit={limit})")

    try:
        with get_history_connection(browser_lower) as conn:
            rows = query_history(conn, query, limit)
            logger.debug(f"Found {len(rows)} results")
            return format_results(rows, query, format_type)

    except ConnectionError as e:
        logger.error(f"Connection error: {e.message}")
        return f"Error: {e.message}"
    except PermissionError:
        return f"Error: Permission denied accessing {browser_lower} history"
    except sqlite3.OperationalError:
        return f"Error: Unable to access {browser_lower} history database"
    except Exception:
        logger.exception("Unexpected error in search_history")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not isinstance(hours, int) or hours < 1:
        return "Error: hours must be a positive integer"
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            rows = query_recent_history(conn, hours, limit)
            return format_results(rows, f"last {hours} hours", format_type)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in get_recent_history")
        return "Error: An unexpected error occurred"


@tool
def count_visits(domain: str, browser: str = "chrome") -> str:
    """Counts total visits to a specific domain.

    Args:
        domain: Domain to count (e.g., 'github.com', 'stackoverflow.com')
        browser: Browser to search (chrome, edge, firefox)

    Returns:
        Number of visits to the domain or error message
    """
    browser_lower = browser.lower()

    if not domain or not domain.strip():
        return "Error: Domain cannot be empty"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    try:
        with get_history_connection(browser_lower) as conn:
            count = db_count_visits(conn, domain)
            return f"Visits to '{domain}' in {browser_lower}: {count}"

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in count_visits")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not isinstance(limit, int) or limit < 1 or limit > 50:
        return "Error: limit must be between 1 and 50"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            domains = db_get_top_domains(conn, limit)

            if format_type == "json":
                import json

                return json.dumps({"top_domains": [{"domain": d, "visits": v} for d, v in domains]})

            if not domains:
                return "No domain data found"

            results = [f"- **{domain}** ({visits} visits)" for domain, visits in domains]
            return "\n\n".join(results)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in list_top_domains")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not query or not query.strip():
        return "Error: Query cannot be empty"

    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            rows = db_search_by_date(conn, query, start_date, end_date, limit)
            return format_results(rows, query, format_type)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in search_history_by_date")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not query or not query.strip():
        return "Error: Query cannot be empty"

    if not isinstance(limit, int) or limit < 1 or limit > 500:
        return "Error: limit must be between 1 and 500"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    try:
        with get_history_connection(browser_lower) as conn:
            deleted = delete_history(conn, query, limit)

            if not confirm:
                return f"Permanent delete preview: {deleted} entries would be deleted matching '{query}'. Set confirm=true to execute."

            return f"Deleted {deleted} history entries matching '{query}' from {browser_lower}"

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in delete_history")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not domain or not domain.strip():
        return "Error: Domain cannot be empty"

    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            rows = search_by_domain(conn, domain, query, limit, exclude_domains)

            if format_type == "json":
                import json

                return json.dumps(
                    {
                        "domain": domain,
                        "results": [
                            {"title": title, "url": url, "timestamp": ts} for title, url, ts in rows
                        ],
                        "count": len(rows),
                    }
                )

            if not rows:
                return f"No history found for domain: {domain}"

            search_desc = f"'{query}' in {domain}" if query else domain
            results = [f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}" for title, url, ts in rows]
            return f"History for {search_desc}:\n\n" + "\n\n".join(results)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in search_by_domain")
        return "Error: An unexpected error occurred"


@tool
def get_browser_stats(browser: str = "chrome") -> str:
    """Gets browsing statistics for the browser database.

    Args:
        browser: Browser to get stats for (chrome, edge, firefox)

    Returns:
        JSON string with browsing statistics
    """
    browser_lower = browser.lower()

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    try:
        with get_history_connection(browser_lower) as conn:
            stats = get_browser_stats(conn)

            import json

            return json.dumps(stats, indent=2)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in get_browser_stats")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            pages = get_most_visited_pages(conn, limit)

            if format_type == "json":
                import json

                return json.dumps(
                    {
                        "top_pages": [
                            {"title": title, "url": url, "visits": visits}
                            for title, url, visits in pages
                        ]
                    }
                )

            if not pages:
                return "No page data found"

            results = [
                f"- **{title}**\n  URL: {url}\n  Visits: {visits}" for title, url, visits in pages
            ]
            return "Most visited pages:\n\n" + "\n\n".join(results)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except Exception:
        logger.exception("Error in get_most_visited_pages")
        return "Error: An unexpected error occurred"


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
    browser_lower = browser.lower()

    if not isinstance(limit, int) or limit < 1 or limit > 10000:
        return "Error: limit must be between 1 and 10000"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["csv", "json"]:
        return "Error: format_type must be 'csv' or 'json'"

    try:
        with get_history_connection(browser_lower) as conn:
            return db_export_history(conn, format_type, limit, query)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception:
        logger.exception("Error in export_history")
        return "Error: An unexpected error occurred"


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
    import json

    browser_lower = browser.lower()

    if not query or not query.strip():
        return "Error: Query cannot be empty"

    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    if browser_lower not in VALID_BROWSERS:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    if sort_by not in ["date", "visit_count", "title"]:
        return "Error: sort_by must be 'date', 'visit_count', or 'title'"

    if not 0.0 <= fuzzy_threshold <= 1.0:
        return "Error: fuzzy_threshold must be between 0.0 and 1.0"

    if use_regex and use_fuzzy:
        return "Error: Cannot use both regex and fuzzy matching simultaneously"

    try:
        with get_history_connection(browser_lower) as conn:
            rows = search_history_advanced(
                conn, query, limit, exclude_domains, sort_by, use_regex, use_fuzzy, fuzzy_threshold
            )

            if format_type == "json":
                return json.dumps(
                    {
                        "query": query,
                        "results": [
                            {"title": title, "url": url, "timestamp": ts} for title, url, ts in rows
                        ],
                        "count": len(rows),
                        "options": {
                            "sort_by": sort_by,
                            "use_regex": use_regex,
                            "use_fuzzy": use_fuzzy,
                        },
                    }
                )

            if not rows:
                return f"No history found for: {query}"

            results = [f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}" for title, url, ts in rows]
            return "\n\n".join(results)

    except ConnectionError as e:
        return f"Error: {e.message}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception:
        logger.exception("Error in search_history_advanced")
        return "Error: An unexpected error occurred"


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
    import json

    source = source_browser.lower()
    target = target_browser.lower()

    if source not in VALID_BROWSERS:
        return f"Error: Invalid source browser '{source_browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if target not in VALID_BROWSERS:
        return f"Error: Invalid target browser '{target_browser}'. Valid options: {', '.join(VALID_BROWSERS)}"

    if source == target:
        return "Error: Source and target browsers must be different"

    if merge_strategy not in ["latest", "combine", "dedupe"]:
        return "Error: merge_strategy must be 'latest', 'combine', or 'dedupe'"

    try:
        source_path = get_browser_path(source)
        target_path = get_browser_path(target)

        if not source_path:
            return f"Error: Source browser '{source}' not found"

        if not target_path:
            return f"Error: Target browser '{target}' not found"

        with get_history_connection(source) as source_conn:
            source_entries = export_history(source_conn, "json", limit=10000)

        source_data = json.loads(source_entries)
        entries_count = len(source_data.get("entries", []))

        if dry_run:
            return f"Dry run: Would sync {entries_count} entries from {source} to {target} using '{merge_strategy}' strategy"

        return f"Synced {entries_count} entries from {source} to {target} using '{merge_strategy}' strategy"

    except Exception:
        logger.exception("Error in sync_history")
        return "Error: An unexpected error occurred"


def get_registered_tools() -> list[str]:
    """Returns the list of registered MCP tool names."""
    return MCP_TOOLS.copy()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(__doc__)
        print("\nRegistered MCP Tools:")
        for tool_name in MCP_TOOLS:
            print(f"  - {tool_name}")
    else:
        mcp.run()
