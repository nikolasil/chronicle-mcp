"""Domain search service for ChronicleMCP.

This module provides domain-specific search operations for browser history.
"""

from typing import Any

from chronicle_mcp.core._connection import with_connection
from chronicle_mcp.core.formatters import format_domain_search_results
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_domain,
    validate_exclude_domains,
    validate_format_type,
    validate_limit,
)
from chronicle_mcp.database import search_by_domain as db_search_by_domain


def search_by_domain(
    domain: str,
    query: str | None = None,
    limit: int = 20,
    browser: str = "chrome",
    format_type: str = "markdown",
    exclude_domains: list[str] | None = None,
) -> dict[str, Any]:
    """Search history within a specific domain.

    Args:
        domain: Domain to search within
        query: Optional search term within domain
        limit: Maximum results (1-100)
        browser: Browser to search
        format_type: 'markdown' or 'json'
        exclude_domains: Domains to exclude

    Returns:
        Dictionary with results and formatted message
    """
    browser_lower = validate_browser(browser)
    domain_clean = validate_domain(domain)
    limit_val = validate_limit(limit, 1, 100)
    format_clean = validate_format_type(format_type)
    exclude_clean = validate_exclude_domains(exclude_domains)

    rows = with_connection(
        browser_lower,
        lambda conn: db_search_by_domain(conn, domain_clean, query, limit_val, exclude_clean),
    )

    return {
        "results": rows,
        "count": len(rows),
        "domain": domain_clean,
        "query": query,
        "message": format_domain_search_results(rows, domain_clean, query, format_clean),
    }
