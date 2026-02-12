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
    count_domain_visits,
    format_results,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import get_top_domains as db_get_top_domains
from chronicle_mcp.database import search_by_date as db_search_by_date
from chronicle_mcp.paths import get_available_browsers

setup_logging()
logger = logging.getLogger(__name__)

mcp = FastMCP("Chronicle")

VALID_BROWSERS = ["chrome", "edge", "firefox"]

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
            count = count_domain_visits(conn, domain)
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


def get_registered_tools() -> list[str]:
    """Returns the list of registered MCP tool names."""
    return MCP_TOOLS.copy()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(__doc__)
            print("\nRegistered MCP Tools:")
            for tool_name in MCP_TOOLS:
                print(f"  - {tool_name}")
            print("\nOptions:")
            print("  dev     Run with MCP Inspector for testing")
            print("  --help  Show this help message")
        elif sys.argv[1] == "dev":
            print("Starting MCP Inspector...")
            mcp.run()
        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Use: python server.py [--help|dev]")
    else:
        mcp.run()
