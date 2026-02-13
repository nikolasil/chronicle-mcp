"""Core business logic layer for ChronicleMCP.

This module provides all service operations for browser history management.
It handles validation, database operations, and returns structured data.
Protocol adapters (MCP, HTTP) consume these services and format responses.
"""

import logging
from collections.abc import Callable
from typing import Any

from chronicle_mcp.connection import (
    BrowserNotFoundError as ConnBrowserNotFoundError,
    ConnectionError as ConnConnectionError,
    DatabaseLockedError as ConnDatabaseLockedError,
    PermissionError as ConnPermissionError,
    get_history_connection,
)
from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
    ServiceError,
)
from chronicle_mcp.core.formatters import (
    format_advanced_search_results,
    format_available_browsers,
    format_browser_stats,
    format_delete_preview,
    format_delete_result,
    format_domain_search_results,
    format_domain_visits,
    format_export,
    format_most_visited_pages,
    format_recent_results,
    format_search_results,
    format_sync_preview,
    format_sync_result,
    format_top_domains,
)
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_browsers_different,
    validate_date_range,
    validate_domain,
    validate_exclude_domains,
    validate_format_type,
    validate_fuzzy_threshold,
    validate_hours,
    validate_limit,
    validate_merge_strategy,
    validate_query,
    validate_search_options,
    validate_sort_by,
)
from chronicle_mcp.database import (
    count_domain_visits,
    delete_history as db_delete_history,
    export_history as db_export_history,
    get_browser_stats as db_get_browser_stats,
    get_most_visited_pages as db_get_most_visited_pages,
    get_top_domains as db_get_top_domains,
    query_history,
    query_recent_history,
    search_by_date as db_search_by_date,
    search_by_domain as db_search_by_domain,
    search_history_advanced as db_search_history_advanced,
)
from chronicle_mcp.paths import get_available_browsers, get_browser_path

logger = logging.getLogger(__name__)


class HistoryService:
    """Service layer for browser history operations."""

    @staticmethod
    def _with_connection(browser: str, operation: Callable[..., Any]) -> Any:
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
        except ConnPermissionError:
            raise PermissionDeniedError(browser, "")
        except ConnConnectionError as e:
            logger.error(f"Connection error: {e.message}")
            raise DatabaseError(f"Failed to access {browser} history: {e.message}")
        except Exception as e:
            logger.exception("Unexpected database error")
            raise DatabaseError(f"Database operation failed: {e}")

    @classmethod
    def list_available_browsers(cls) -> dict[str, Any]:
        """Get list of available browsers.

        Returns:
            Dictionary with list of browsers and formatted message
        """
        browsers = get_available_browsers()
        return {
            "browsers": browsers,
            "message": format_available_browsers(browsers)
        }

    @classmethod
    def search_history(
        cls,
        query: str,
        limit: int = 5,
        browser: str = "chrome",
        format_type: str = "markdown"
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

        rows = cls._with_connection(
            browser_lower,
            lambda conn: query_history(conn, query_clean, limit_val)
        )

        return {
            "results": rows,
            "count": len(rows),
            "query": query_clean,
            "message": format_search_results(rows, query_clean, format_clean)
        }

    @classmethod
    def get_recent_history(
        cls,
        hours: int = 24,
        limit: int = 20,
        browser: str = "chrome",
        format_type: str = "markdown"
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

        rows = cls._with_connection(
            browser_lower,
            lambda conn: query_recent_history(conn, hours_val, limit_val)
        )

        return {
            "results": rows,
            "count": len(rows),
            "hours": hours_val,
            "message": format_recent_results(rows, hours_val, format_clean)
        }

    @classmethod
    def count_visits(cls, domain: str, browser: str = "chrome") -> dict[str, Any]:
        """Count visits to a domain.

        Args:
            domain: Domain to count
            browser: Browser to search

        Returns:
            Dictionary with count and formatted message
        """
        browser_lower = validate_browser(browser)
        domain_clean = validate_domain(domain)

        count = cls._with_connection(
            browser_lower,
            lambda conn: count_domain_visits(conn, domain_clean)
        )

        return {
            "domain": domain_clean,
            "browser": browser_lower,
            "count": count,
            "message": format_domain_visits(domain_clean, browser_lower, count)
        }

    @classmethod
    def list_top_domains(
        cls,
        limit: int = 10,
        browser: str = "chrome",
        format_type: str = "markdown"
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

        domains = cls._with_connection(
            browser_lower,
            lambda conn: db_get_top_domains(conn, limit_val)
        )

        return {
            "domains": domains,
            "count": len(domains),
            "message": format_top_domains(domains, format_clean)
        }

    @classmethod
    def search_history_by_date(
        cls,
        query: str,
        start_date: str,
        end_date: str,
        limit: int = 10,
        browser: str = "chrome",
        format_type: str = "markdown"
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

        rows = cls._with_connection(
            browser_lower,
            lambda conn: db_search_by_date(conn, query_clean, start_clean, end_clean, limit_val)
        )

        return {
            "results": rows,
            "count": len(rows),
            "query": query_clean,
            "start_date": start_clean,
            "end_date": end_clean,
            "message": format_search_results(rows, query_clean, format_clean)
        }

    @classmethod
    def delete_history(
        cls,
        query: str,
        limit: int = 100,
        browser: str = "chrome",
        confirm: bool = False
    ) -> dict[str, Any]:
        """Delete history entries matching a query.

        Args:
            query: Search term to match
            limit: Maximum entries to delete (1-500)
            browser: Browser to search
            confirm: If True, actually delete; if False, preview only

        Returns:
            Dictionary with deletion info and formatted message
        """
        browser_lower = validate_browser(browser)
        query_clean = validate_query(query)
        limit_val = validate_limit(limit, 1, 500)

        if not confirm:
            # Preview mode - just count matches
            rows = cls._with_connection(
                browser_lower,
                lambda conn: query_history(conn, query_clean, limit_val)
            )
            count = len(rows)

            return {
                "preview": True,
                "query": query_clean,
                "count": count,
                "message": format_delete_preview(query_clean, count)
            }

        # Actually delete
        deleted = cls._with_connection(
            browser_lower,
            lambda conn: db_delete_history(conn, query_clean, limit_val)
        )

        return {
            "deleted": deleted,
            "query": query_clean,
            "browser": browser_lower,
            "message": format_delete_result(query_clean, browser_lower, deleted)
        }

    @classmethod
    def search_by_domain(
        cls,
        domain: str,
        query: str | None = None,
        limit: int = 20,
        browser: str = "chrome",
        format_type: str = "markdown",
        exclude_domains: list[str] | None = None
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

        rows = cls._with_connection(
            browser_lower,
            lambda conn: db_search_by_domain(
                conn, domain_clean, query, limit_val, exclude_clean
            )
        )

        return {
            "results": rows,
            "count": len(rows),
            "domain": domain_clean,
            "query": query,
            "message": format_domain_search_results(rows, domain_clean, query, format_clean)
        }

    @classmethod
    def get_browser_stats(cls, browser: str = "chrome") -> dict[str, Any]:
        """Get browser statistics.

        Args:
            browser: Browser to analyze

        Returns:
            Dictionary with statistics and formatted message
        """
        browser_lower = validate_browser(browser)

        stats = cls._with_connection(browser_lower, db_get_browser_stats)

        return {
            "stats": stats,
            "message": format_browser_stats(stats)
        }

    @classmethod
    def get_most_visited_pages(
        cls,
        limit: int = 20,
        browser: str = "chrome",
        format_type: str = "markdown"
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

        pages = cls._with_connection(
            browser_lower,
            lambda conn: db_get_most_visited_pages(conn, limit_val)
        )

        return {
            "pages": pages,
            "count": len(pages),
            "message": format_most_visited_pages(pages, format_clean)
        }

    @classmethod
    def export_history(
        cls,
        format_type: str = "csv",
        limit: int = 1000,
        query: str | None = None,
        browser: str = "chrome"
    ) -> dict[str, Any]:
        """Export history to CSV or JSON.

        Args:
            format_type: 'csv' or 'json'
            limit: Maximum entries (1-10000)
            query: Optional search filter
            browser: Browser to export

        Returns:
            Dictionary with exported data and formatted content
        """
        browser_lower = validate_browser(browser)
        format_clean = validate_format_type(format_type, export=True)
        limit_val = validate_limit(limit, 1, 10000)

        content = cls._with_connection(
            browser_lower,
            lambda conn: db_export_history(conn, format_clean, limit_val, query)
        )

        return {
            "content": content,
            "format": format_clean,
            "browser": browser_lower
        }

    @classmethod
    def search_history_advanced(
        cls,
        query: str,
        limit: int = 20,
        browser: str = "chrome",
        format_type: str = "markdown",
        exclude_domains: list[str] | None = None,
        sort_by: str = "date",
        use_regex: bool = False,
        use_fuzzy: bool = False,
        fuzzy_threshold: float = 0.6
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
            "fuzzy_threshold": threshold_val if use_fuzzy else None
        }

        rows = cls._with_connection(
            browser_lower,
            lambda conn: db_search_history_advanced(
                conn, query_clean, limit_val, exclude_clean,
                sort_clean, use_regex, use_fuzzy, threshold_val
            )
        )

        return {
            "results": rows,
            "count": len(rows),
            "query": query_clean,
            "options": options,
            "message": format_advanced_search_results(rows, query_clean, format_clean, options)
        }

    @classmethod
    def sync_history(
        cls,
        source_browser: str,
        target_browser: str,
        merge_strategy: str = "latest",
        dry_run: bool = True
    ) -> dict[str, Any]:
        """Sync history between browsers.

        Args:
            source_browser: Source browser name
            target_browser: Target browser name
            merge_strategy: How to merge ('latest', 'combine', 'dedupe')
            dry_run: If True, preview only

        Returns:
            Dictionary with sync info and formatted message
        """
        source = validate_browser(source_browser)
        target = validate_browser(target_browser)
        validate_browsers_different(source, target)
        strategy = validate_merge_strategy(merge_strategy)

        # Check paths exist
        source_path = get_browser_path(source)
        target_path = get_browser_path(target)

        if not source_path:
            raise BrowserNotFoundError(source)

        if not target_path:
            raise BrowserNotFoundError(target)

        # Get source entries count
        import json
        entries_json = cls._with_connection(
            source,
            lambda conn: db_export_history(conn, "json", 10000)
        )
        entries_data = json.loads(entries_json)
        entries_count = len(entries_data.get("entries", []))

        if dry_run:
            return {
                "dry_run": True,
                "source": source,
                "target": target,
                "entries_count": entries_count,
                "merge_strategy": strategy,
                "message": format_sync_preview(source, target, entries_count, strategy)
            }

        # TODO: Implement actual sync logic
        return {
            "dry_run": False,
            "source": source,
            "target": target,
            "entries_count": entries_count,
            "merge_strategy": strategy,
            "message": format_sync_result(source, target, entries_count, strategy)
        }
