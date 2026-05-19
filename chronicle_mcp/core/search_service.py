"""Search service layer for ChronicleMCP.

This module provides all search-related operations for browser history.
It handles validation, database operations, and returns structured data.
"""

import logging
from typing import Any

from chronicle_mcp.connection import (
    BrowserNotFoundError as ConnBrowserNotFoundError,
)
from chronicle_mcp.connection import (
    ConnectionError as ConnConnectionError,
)
from chronicle_mcp.connection import (
    DatabaseLockedError as ConnDatabaseLockedError,
)
from chronicle_mcp.connection import (
    PermissionDeniedError as ConnPermissionDeniedError,
)
from chronicle_mcp.connection import (
    get_history_connection,
)
from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
)
from chronicle_mcp.core.formatters import (
    format_advanced_search_results,
    format_domain_visits,
    format_most_visited_pages,
    format_recent_results,
    format_search_results,
    format_top_domains,
)
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_date_range,
    validate_domain,
    validate_exclude_domains,
    validate_format_type,
    validate_fuzzy_threshold,
    validate_hours,
    validate_limit,
    validate_query,
    validate_search_options,
    validate_sort_by,
)
from chronicle_mcp.database import (
    count_domain_visits,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import (
    get_most_visited_pages as db_get_most_visited_pages,
)
from chronicle_mcp.database import (
    get_top_domains as db_get_top_domains,
)
from chronicle_mcp.database import (
    search_by_date as db_search_by_date,
)
from chronicle_mcp.database import (
    search_history_advanced as db_search_history_advanced,
)

logger = logging.getLogger(__name__)


def _with_connection(browser: str, operation: Any) -> Any:
    """Execute an operation with a database connection.

    Args:
        browser: Browser name
        operation: Function that takes a connection and returns data

    Returns:
        Result of the operation

    Raises:
        BrowserNotFoundError: If browser not found
        DatabaseLockedError: If database is locked
        PermissionDeniedError: If permission denied
        DatabaseError: For other database errors
    """
    try:
        with get_history_connection(browser) as conn:
            return operation(conn)
    except ConnBrowserNotFoundError:
        raise BrowserNotFoundError(browser)
    except ConnDatabaseLockedError:
        raise DatabaseLockedError(browser)
    except ConnPermissionDeniedError:
        raise PermissionDeniedError(browser, "")
    except ConnConnectionError as e:
        logger.error(f"Connection error: {e.message}")
        raise DatabaseError(f"Failed to access {browser} history: {e.message}")
    except Exception as e:
        logger.exception("Unexpected database error")
        raise DatabaseError(f"Database operation failed: {e}")


def search_history(
    query: str, limit: int = 5, browser: str = "chrome", format_type: str = "markdown"
) -> dict[str, Any]:
    """Search browser history.

    Args:
        query: Search term
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with results and formatted message
    """
    browser_lower = validate_browser(browser)
    query_clean = validate_query(query)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    logger.info(f"Searching history for '{query_clean}' in {browser_lower} (limit={limit_val})")

    rows = _with_connection(
        browser_lower, lambda conn: query_history(conn, query_clean, limit_val)
    )

    return {
        "results": rows,
        "count": len(rows),
        "query": query_clean,
        "message": format_search_results(rows, query_clean, format_clean),
    }


def get_recent_history(
    hours: int = 24,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Get recent browsing history.

    Args:
        hours: Hours to look back
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with results and formatted message
    """
    browser_lower = validate_browser(browser)
    hours_val = validate_hours(hours)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    rows = _with_connection(
        browser_lower, lambda conn: query_recent_history(conn, hours_val, limit_val)
    )

    return {
        "results": rows,
        "count": len(rows),
        "hours": hours_val,
        "message": format_recent_results(rows, hours_val, format_clean),
    }


def count_visits(domain: str, browser: str = "chrome") -> dict[str, Any]:
    """Count visits to a domain.

    Args:
        domain: Domain to count
        browser: Browser to search

    Returns:
        Dictionary with count and formatted message
    """
    browser_lower = validate_browser(browser)
    domain_clean = validate_domain(domain)

    count = _with_connection(
        browser_lower, lambda conn: count_domain_visits(conn, domain_clean)
    )

    return {
        "domain": domain_clean,
        "browser": browser_lower,
        "count": count,
        "message": format_domain_visits(domain_clean, browser_lower, count),
    }


def list_top_domains(
    limit: int = 10, browser: str = "chrome", format_type: str = "markdown"
) -> dict[str, Any]:
    """Get most visited domains.

    Args:
        limit: Maximum results (1-50)
        browser: Browser to search
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with domains and formatted message
    """
    browser_lower = validate_browser(browser)
    limit_val = validate_limit(limit, 1, 50)
    format_clean = validate_format_type(format_type)

    domains = _with_connection(
        browser_lower, lambda conn: db_get_top_domains(conn, limit_val)
    )

    return {
        "domains": domains,
        "count": len(domains),
        "message": format_top_domains(domains, format_clean),
    }


def get_most_visited_pages(
    limit: int = 20, browser: str = "chrome", format_type: str = "markdown"
) -> dict[str, Any]:
    """Get most visited individual pages.

    Args:
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with pages and formatted message
    """
    browser_lower = validate_browser(browser)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    pages = _with_connection(
        browser_lower, lambda conn: db_get_most_visited_pages(conn, limit_val)
    )

    return {
        "pages": pages,
        "count": len(pages),
        "message": format_most_visited_pages(pages, format_clean),
    }


def search_history_by_date(
    query: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
    browser: str = "chrome",
    format_type: str = "markdown",
) -> dict[str, Any]:
    """Search history within a date range.

    Args:
        query: Search term
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'

    Returns:
        Dictionary with results and formatted message
    """
    browser_lower = validate_browser(browser)
    query_clean = validate_query(query)
    start_clean, end_clean = validate_date_range(start_date, end_date)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)

    rows = _with_connection(
        browser_lower,
        lambda conn: db_search_by_date(conn, query_clean, start_clean, end_clean, limit_val),
    )

    return {
        "results": rows,
        "count": len(rows),
        "query": query_clean,
        "start_date": start_clean,
        "end_date": end_clean,
        "message": format_search_results(rows, query_clean, format_clean),
    }


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
) -> dict[str, Any]:
    """Advanced search with multiple options.

    Args:
        query: Search term
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'
        exclude_domains: Domains to exclude
        sort_by: Sort order ('date', 'visit_count', 'title')
        use_regex: Use regex matching
        use_fuzzy: Use fuzzy matching
        fuzzy_threshold: Minimum similarity (0.0-1.0)

    Returns:
        Dictionary with results and formatted message
    """
    browser_lower = validate_browser(browser)
    query_clean = validate_query(query)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)
    sort_clean = validate_sort_by(sort_by)
    exclude_clean = validate_exclude_domains(exclude_domains)
    threshold_val = validate_fuzzy_threshold(fuzzy_threshold)
    validate_search_options(use_regex, use_fuzzy)

    options = {
        "sort_by": sort_clean,
        "use_regex": use_regex,
        "use_fuzzy": use_fuzzy,
        "fuzzy_threshold": threshold_val if use_fuzzy else None,
    }

    rows = _with_connection(
        browser_lower,
        lambda conn: db_search_history_advanced(
            conn,
            query_clean,
            limit_val,
            exclude_clean,
            sort_clean,
            use_regex,
            use_fuzzy,
            threshold_val,
        ),
    )

    return {
        "results": rows,
        "count": len(rows),
        "query": query_clean,
        "options": options,
        "message": format_advanced_search_results(rows, query_clean, format_clean, options),
    }
