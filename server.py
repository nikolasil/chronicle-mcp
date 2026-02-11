import os
import sqlite3
import shutil
import tempfile
import platform
import time
from contextlib import contextmanager
from fastmcp import FastMCP
from chronicle_mcp.paths import get_browser_path, get_available_browsers, get_all_browser_paths
from chronicle_mcp.database import (
    query_history,
    query_recent_history,
    count_domain_visits,
    get_top_domains as db_get_top_domains,
    search_by_date as db_search_by_date,
    format_results
)

mcp = FastMCP("Chronicle")


@contextmanager
def get_history_connection(browser: str = "chrome"):
    """
    Creates a temporary copy of the history DB to avoid 'Database Locked' errors.

    Args:
        browser: Browser name (chrome, edge, firefox)

    Yields:
        SQLite connection to the history database
    """
    history_path = get_browser_path(browser)

    if not history_path:
        raise FileNotFoundError(f"Could not find {browser} history")

    if not os.path.exists(history_path):
        raise FileNotFoundError(f"Could not find {browser} history at {history_path}")

    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(
        temp_dir,
        f"chronicle_{browser}_temp_{os.getpid()}_{int(time.time() * 1000)}.db"
    )

    try:
        shutil.copy2(history_path, temp_path)
        conn = sqlite3.connect(temp_path)
        try:
            yield conn
        finally:
            conn.close()
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


@mcp.tool()
def list_available_browsers() -> str:
    """
    Returns a list of browsers with detected history databases on this system.

    Returns:
        List of available browsers (chrome, edge, firefox)
    """
    available = get_available_browsers()
    if not available:
        return "No browsers with history found on this system"
    return f"Available browsers: {', '.join(available)}"


@mcp.tool()
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
    """
    Searches browser history for keywords in titles or URLs.

    Args:
        query: Search term to look for in titles or URLs
        limit: Maximum number of results to return (1-100)
        browser: Browser to search (chrome, edge, firefox) - case insensitive
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of matching history entries or error message
    """
    browser = browser.lower()

    if not query or not query.strip():
        return "Error: Query cannot be empty"

    if not isinstance(limit, int):
        return "Error: Limit must be an integer"
    if limit < 1 or limit > 100:
        return "Error: Limit must be between 1 and 100"

    valid_browsers = ["chrome", "edge", "firefox"]
    if browser not in valid_browsers:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(valid_browsers)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser) as conn:
            rows = query_history(conn, query, limit)
            return format_results(rows, query, format_type)

    except FileNotFoundError as e:
        return f"Error: {browser} history not found. Please ensure {browser} is installed."
    except PermissionError as e:
        return f"Error: Permission denied accessing {browser} history"
    except sqlite3.OperationalError as e:
        return f"Error: Unable to access {browser} history database"
    except Exception as e:
        return "Error: An unexpected error occurred"


@mcp.tool()
def get_recent_history(
    hours: int = 24,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
    """
    Gets recent browsing history from the last N hours.

    Args:
        hours: Number of hours to look back (default: 24)
        limit: Maximum number of results (1-100, default: 20)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of recent history entries or error message
    """
    browser = browser.lower()

    if not isinstance(hours, int) or hours < 1:
        return "Error: hours must be a positive integer"
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    valid_browsers = ["chrome", "edge", "firefox"]
    if browser not in valid_browsers:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(valid_browsers)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser) as conn:
            rows = query_recent_history(conn, hours, limit)
            return format_results(rows, f"last {hours} hours", format_type)

    except FileNotFoundError as e:
        return f"Error: {browser} history not found"
    except Exception as e:
        return "Error: An unexpected error occurred"


@mcp.tool()
def count_visits(domain: str, browser: str = "chrome") -> str:
    """
    Counts total visits to a specific domain.

    Args:
        domain: Domain to count (e.g., 'github.com', 'stackoverflow.com')
        browser: Browser to search (chrome, edge, firefox)

    Returns:
        Number of visits to the domain or error message
    """
    browser = browser.lower()

    if not domain or not domain.strip():
        return "Error: Domain cannot be empty"

    valid_browsers = ["chrome", "edge", "firefox"]
    if browser not in valid_browsers:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(valid_browsers)}"

    try:
        with get_history_connection(browser) as conn:
            count = count_domain_visits(conn, domain)
            return f"Visits to '{domain}' in {browser}: {count}"

    except Exception as e:
        return "Error: An unexpected error occurred"


@mcp.tool()
def list_top_domains(
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
    """
    Gets the most visited domains from browser history.

    Args:
        limit: Maximum number of domains to return (1-50, default: 10)
        browser: Browser to search (chrome, edge, firefox)
        format_type: Output format (markdown or json)

    Returns:
        Formatted list of top domains or error message
    """
    browser = browser.lower()

    if not isinstance(limit, int) or limit < 1 or limit > 50:
        return "Error: limit must be between 1 and 50"

    valid_browsers = ["chrome", "edge", "firefox"]
    if browser not in valid_browsers:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(valid_browsers)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser) as conn:
            domains = db_get_top_domains(conn, limit)

            if format_type == "json":
                import json
                return json.dumps({"top_domains": [{"domain": d, "visits": v} for d, v in domains]})

            if not domains:
                return "No domain data found"

            results = [f"- **{domain}** ({visits} visits)" for domain, visits in domains]
            return "\n\n".join(results)

    except Exception as e:
        return "Error: An unexpected error occurred"


@mcp.tool()
def search_history_by_date(
    query: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown"
) -> str:
    """
    Searches browser history within a date range.

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
    browser = browser.lower()

    if not query or not query.strip():
        return "Error: Query cannot be empty"

    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return "Error: limit must be between 1 and 100"

    valid_browsers = ["chrome", "edge", "firefox"]
    if browser not in valid_browsers:
        return f"Error: Invalid browser '{browser}'. Valid options: {', '.join(valid_browsers)}"

    if format_type not in ["markdown", "json"]:
        return "Error: format_type must be 'markdown' or 'json'"

    try:
        with get_history_connection(browser) as conn:
            rows = db_search_by_date(conn, query, start_date, end_date, limit)
            return format_results(rows, query, format_type)

    except Exception as e:
        return "Error: An unexpected error occurred"


if __name__ == "__main__":
    mcp.run()
