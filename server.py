import logging
import os
import shutil
import sqlite3
import tempfile
import time
from contextlib import contextmanager

from fastmcp import FastMCP

from chronicle_mcp.config import setup_logging
from chronicle_mcp.database import (
    count_domain_visits,
    format_results,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import get_top_domains as db_get_top_domains
from chronicle_mcp.database import search_by_date as db_search_by_date
from chronicle_mcp.paths import get_available_browsers, get_browser_path

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

search_history = None
get_recent_history = None
count_visits = None
list_top_domains = None
search_history_by_date = None
list_available_browsers = None


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
def _list_available_browsers() -> str:
    """
    Returns a list of browsers with detected history databases on this system.

    Returns:
        List of available browsers (chrome, edge, firefox)
    """
    available = get_available_browsers()
    if not available:
        return "No browsers with history found on this system"
    return f"Available browsers: {', '.join(available)}"


list_available_browsers = _list_available_browsers


@mcp.tool()
def _search_history(
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
        logger.warning("Empty query received")
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

    logger.info(f"Searching history for '{query}' in {browser} (limit={limit})")
    try:
        with get_history_connection(browser) as conn:
            rows = query_history(conn, query, limit)
            logger.debug(f"Found {len(rows)} results")
            return format_results(rows, query, format_type)

    except FileNotFoundError:
        return f"Error: {browser} history not found. Please ensure {browser} is installed."
    except PermissionError:
        return f"Error: Permission denied accessing {browser} history"
    except sqlite3.OperationalError:
        return f"Error: Unable to access {browser} history database"
    except Exception:
        return "Error: An unexpected error occurred"


search_history = _search_history


@mcp.tool()
def _get_recent_history(
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

    except FileNotFoundError:
        return f"Error: {browser} history not found"
    except Exception:
        return "Error: An unexpected error occurred"


get_recent_history = _get_recent_history


@mcp.tool()
def _count_visits(domain: str, browser: str = "chrome") -> str:
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

    except Exception:
        return "Error: An unexpected error occurred"


count_visits = _count_visits


@mcp.tool()
def _list_top_domains(
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

    except Exception:
        return "Error: An unexpected error occurred"


list_top_domains = _list_top_domains


@mcp.tool()
def _search_history_by_date(
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

    except Exception:
        return "Error: An unexpected error occurred"


search_history_by_date = _search_history_by_date


if __name__ == "__main__":
    mcp.run()
