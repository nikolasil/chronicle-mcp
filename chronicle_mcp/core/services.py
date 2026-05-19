"""Core business logic layer for ChronicleMCP.

This module provides all service operations for browser history management.
It handles validation, database operations, and returns structured data.
Protocol adapters (MCP, HTTP) consume these services and format responses.
"""

import json
import logging
from collections.abc import Callable
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
    format_available_browsers,
    format_bookmarks,
    format_browser_stats,
    format_delete_preview,
    format_delete_result,
    format_domain_search_results,
    format_domain_visits,
    format_downloads,
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
    detect_schema,
    get_category_stats,
    get_history_entries,
    get_hourly_stats_for_period,
    get_uncategorized_urls,
    get_visit_patterns_by_hour,
    query_bookmarks,
    query_downloads,
    query_history,
    query_recent_history,
)
from chronicle_mcp.database import (
    delete_history as db_delete_history,
)
from chronicle_mcp.database import (
    export_history as db_export_history,
)
from chronicle_mcp.database import (
    get_browser_stats as db_get_browser_stats,
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
    search_by_domain as db_search_by_domain,
)
from chronicle_mcp.database import (
    search_history_advanced as db_search_history_advanced,
)
from chronicle_mcp.paths import (
    get_available_bookmarks,
    get_available_browsers,
    get_available_downloads,
    get_bookmark_path,
    get_browser_path,
    get_browser_schema,
    get_download_path,
)

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
        except ConnPermissionDeniedError:
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
        return {"browsers": browsers, "message": format_available_browsers(browsers)}

    @classmethod
    def search_history(
        cls, query: str, limit: int = 5, browser: str = "chrome", format_type: str = "markdown"
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
            browser_lower, lambda conn: query_history(conn, query_clean, limit_val)
        )

        return {
            "results": rows,
            "count": len(rows),
            "query": query_clean,
            "message": format_search_results(rows, query_clean, format_clean),
        }

    @classmethod
    def get_recent_history(
        cls,
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

        rows = cls._with_connection(
            browser_lower, lambda conn: query_recent_history(conn, hours_val, limit_val)
        )

        return {
            "results": rows,
            "count": len(rows),
            "hours": hours_val,
            "message": format_recent_results(rows, hours_val, format_clean),
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
            browser_lower, lambda conn: count_domain_visits(conn, domain_clean)
        )

        return {
            "domain": domain_clean,
            "browser": browser_lower,
            "count": count,
            "message": format_domain_visits(domain_clean, browser_lower, count),
        }

    @classmethod
    def list_top_domains(
        cls, limit: int = 10, browser: str = "chrome", format_type: str = "markdown"
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
            browser_lower, lambda conn: db_get_top_domains(conn, limit_val)
        )

        return {
            "domains": domains,
            "count": len(domains),
            "message": format_top_domains(domains, format_clean),
        }

    @classmethod
    def search_history_by_date(
        cls,
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

        rows = cls._with_connection(
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

    @classmethod
    def delete_history(
        cls, query: str, limit: int = 100, browser: str = "chrome", confirm: bool = False
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
                browser_lower, lambda conn: query_history(conn, query_clean, limit_val)
            )
            count = len(rows)

            return {
                "preview": True,
                "query": query_clean,
                "count": count,
                "message": format_delete_preview(query_clean, count),
            }

        # Actually delete
        deleted = cls._with_connection(
            browser_lower, lambda conn: db_delete_history(conn, query_clean, limit_val)
        )

        return {
            "deleted": deleted,
            "query": query_clean,
            "browser": browser_lower,
            "message": format_delete_result(query_clean, browser_lower, deleted),
        }

    @classmethod
    def search_by_domain(
        cls,
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

        rows = cls._with_connection(
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

    @classmethod
    def get_browser_stats(
        cls, browser: str = "chrome", format_type: str = "markdown"
    ) -> dict[str, Any]:
        """Get browser statistics.

        Args:
            browser: Browser to analyze
            format_type: 'markdown' or 'json'

        Returns:
            Dictionary with statistics and formatted message
        """
        browser_lower = validate_browser(browser)
        format_clean = validate_format_type(format_type)

        stats = cls._with_connection(browser_lower, db_get_browser_stats)

        return {"stats": stats, "message": format_browser_stats(stats, format_clean)}

    @classmethod
    def get_most_visited_pages(
        cls, limit: int = 20, browser: str = "chrome", format_type: str = "markdown"
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
            browser_lower, lambda conn: db_get_most_visited_pages(conn, limit_val)
        )

        return {
            "pages": pages,
            "count": len(pages),
            "message": format_most_visited_pages(pages, format_clean),
        }

    @classmethod
    def export_history(
        cls,
        format_type: str = "csv",
        limit: int = 1000,
        query: str | None = None,
        browser: str = "chrome",
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
            browser_lower, lambda conn: db_export_history(conn, format_clean, limit_val, query)
        )

        return {"content": content, "format": format_clean, "browser": browser_lower}

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

        rows = cls._with_connection(
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

    @classmethod
    def sync_history(
        cls,
        source_browser: str,
        target_browser: str,
        merge_strategy: str = "latest",
        dry_run: bool = True,
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

        entries_json = cls._with_connection(
            source, lambda conn: db_export_history(conn, "json", 10000)
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
                "message": format_sync_preview(source, target, entries_count, strategy),
            }

        from chronicle_mcp.database import sync_to_browser

        with get_history_connection(source) as conn_source:
            entries = get_history_entries(conn_source, 10000)

        synced_count = sync_to_browser(target_path, entries, strategy)

        return {
            "dry_run": False,
            "source": source,
            "target": target,
            "entries_count": synced_count,
            "merge_strategy": strategy,
            "message": format_sync_result(source, target, synced_count, strategy),
        }

    @classmethod
    def list_available_bookmarks(cls) -> dict[str, Any]:
        """Get list of browsers with available bookmarks.

        Returns:
            Dictionary with list of browsers and formatted message
        """
        browsers = get_available_bookmarks()
        return {"browsers": browsers, "message": format_available_browsers(browsers)}

    @classmethod
    def list_available_downloads(cls) -> dict[str, Any]:
        """Get list of browsers with available downloads history.

        Returns:
            Dictionary with list of browsers and formatted message
        """
        browsers = get_available_downloads()
        return {"browsers": browsers, "message": format_available_browsers(browsers)}

    @classmethod
    def get_bookmarks(
        cls,
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

    @classmethod
    def get_downloads(
        cls,
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

    @classmethod
    def compare_time_periods(
        cls,
        start_date1: str,
        end_date1: str,
        start_date2: str,
        end_date2: str,
        browser: str = "chrome",
    ) -> dict[str, Any]:
        """Compare browsing statistics between two time periods.

        Args:
            start_date1: Start date of first period (ISO format)
            end_date1: End date of first period (ISO format)
            start_date2: Start date of second period (ISO format)
            end_date2: End date of second period (ISO format)
            browser: Browser to analyze

        Returns:
            Dictionary with comparison data for both periods
        """
        from chronicle_mcp.core.categories import CATEGORY_PATTERNS

        browser_lower = validate_browser(browser)
        validate_date_range(start_date1, end_date1)
        validate_date_range(start_date2, end_date2)

        period1_stats = cls._with_connection(
            browser_lower,
            lambda conn: get_hourly_stats_for_period(conn, start_date1, end_date1),
        )

        period2_stats = cls._with_connection(
            browser_lower,
            lambda conn: get_hourly_stats_for_period(conn, start_date2, end_date2),
        )

        category_stats = cls._with_connection(
            browser_lower,
            lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
        )

        total_delta = period2_stats["total_visits"] - period1_stats["total_visits"]
        unique_delta = period2_stats["unique_urls"] - period1_stats["unique_urls"]

        top_domains_period1 = set(d for d, _ in period1_stats.get("top_domains", []))
        top_domains_period2 = set(d for d, _ in period2_stats.get("top_domains", []))
        domains_gained = list(top_domains_period2 - top_domains_period1)[:5]
        domains_lost = list(top_domains_period1 - top_domains_period2)[:5]

        return {
            "period1": {
                "start": start_date1,
                "end": end_date1,
                "total_visits": period1_stats["total_visits"],
                "unique_urls": period1_stats["unique_urls"],
                "top_domains": period1_stats.get("top_domains", []),
            },
            "period2": {
                "start": start_date2,
                "end": end_date2,
                "total_visits": period2_stats["total_visits"],
                "unique_urls": period2_stats["unique_urls"],
                "top_domains": period2_stats.get("top_domains", []),
            },
            "changes": {
                "total_visits_delta": total_delta,
                "unique_urls_delta": unique_delta,
                "top_domains_gained": domains_gained,
                "top_domains_lost": domains_lost,
            },
            "category_breakdown": category_stats,
        }

    @classmethod
    def analyze_productivity(
        cls,
        start_date: str | None = None,
        end_date: str | None = None,
        browser: str = "chrome",
    ) -> dict[str, Any]:
        """Analyze browsing productivity.

        Args:
            start_date: Optional start date (ISO format)
            end_date: Optional end date (ISO format)
            browser: Browser to analyze

        Returns:
            Dictionary with productivity score, breakdown, and recommendations
        """
        from chronicle_mcp.core.categories import (
            CATEGORY_PATTERNS,
            calculate_productivity_score,
            generate_recommendations,
            get_category_breakdown,
        )

        browser_lower = validate_browser(browser)

        category_stats = cls._with_connection(
            browser_lower,
            lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
        )

        breakdown = get_category_breakdown(category_stats)
        score, grade = calculate_productivity_score(category_stats)

        top_domains = cls._with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 10))

        recommendations = generate_recommendations(category_stats, top_domains)

        return {
            "productivity_score": score,
            "grade": grade,
            "category_breakdown": breakdown,
            "recommendations": recommendations,
            "browser": browser_lower,
            "period": {
                "start": start_date,
                "end": end_date,
            },
        }

    @classmethod
    def suggest_categories(
        cls,
        browser: str = "chrome",
        limit: int = 20,
    ) -> dict[str, Any]:
        """Suggest categories for uncategorized URLs.

        Args:
            browser: Browser to analyze
            limit: Maximum number of suggestions

        Returns:
            Dictionary with uncategorized URLs that could be categorized
        """
        from chronicle_mcp.core.categories import CATEGORY_PATTERNS, categorize_url

        browser_lower = validate_browser(browser)
        limit_val = validate_limit(limit, 1, 100)

        uncategorized = cls._with_connection(
            browser_lower,
            lambda conn: get_uncategorized_urls(conn, CATEGORY_PATTERNS, limit_val),
        )

        suggestions = []
        for title, url, visit_count in uncategorized:
            category = categorize_url(url)
            if category:
                suggestions.append(
                    {
                        "title": title,
                        "url": url,
                        "visit_count": visit_count,
                        "suggested_category": category,
                    }
                )

        return {
            "uncategorized": suggestions,
            "count": len(suggestions),
            "browser": browser_lower,
        }

    @classmethod
    def export_visualization(
        cls,
        format_type: str = "chart_json",
        period: str = "month",
        browser: str = "chrome",
    ) -> dict[str, Any]:
        """Export data formatted for visualization.

        Args:
            format_type: 'chart_json' for Chart.js or 'csv'
            period: Time period - 'day', 'week', or 'month'
            browser: Browser to export from

        Returns:
            Dictionary with visualization-ready data
        """

        from chronicle_mcp.core.categories import (
            CATEGORY_PATTERNS,
            get_category_breakdown,
        )

        browser_lower = validate_browser(browser)

        category_stats = cls._with_connection(
            browser_lower,
            lambda conn: get_category_stats(conn, CATEGORY_PATTERNS),
        )

        breakdown = get_category_breakdown(category_stats)

        visit_patterns = cls._with_connection(
            browser_lower, lambda conn: get_visit_patterns_by_hour(conn)
        )

        top_domains = cls._with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 10))

        if format_type == "csv":
            import csv
            from io import StringIO

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(["Category", "Count", "Percentage", "Weight"])

            for cat, data in breakdown.items():
                writer.writerow(
                    [
                        cat,
                        data.get("count", 0),
                        data.get("percentage", 0),
                        data.get("weight", 0),
                    ]
                )

            return {
                "content": output.getvalue(),
                "format": "csv",
                "period": period,
            }

        chart_data = {
            "charts": [
                {
                    "type": "doughnut",
                    "title": "Time by Category",
                    "data": {
                        "labels": list(breakdown.keys()),
                        "datasets": [
                            {
                                "data": [breakdown[c].get("count", 0) for c in breakdown],
                                "backgroundColor": [
                                    "#4CAF50",
                                    "#2196F3",
                                    "#FF9800",
                                    "#E91E63",
                                    "#9C27B0",
                                    "#00BCD4",
                                    "#795548",
                                ],
                            }
                        ],
                    },
                },
                {
                    "type": "bar",
                    "title": "Top 10 Domains",
                    "data": {
                        "labels": [d for d, _ in top_domains],
                        "datasets": [
                            {
                                "label": "Visits",
                                "data": [c for _, c in top_domains],
                                "backgroundColor": "#2196F3",
                            }
                        ],
                    },
                },
                {
                    "type": "bar",
                    "title": "Activity by Hour",
                    "data": {
                        "labels": list(range(24)),
                        "datasets": [
                            {
                                "label": "Visits",
                                "data": [visit_patterns.get(h, 0) for h in range(24)],
                                "backgroundColor": "#4CAF50",
                            }
                        ],
                    },
                },
            ],
            "period": period,
            "category_breakdown": breakdown,
        }

        return {
            "charts": chart_data["charts"],
            "period": period,
            "category_breakdown": breakdown,
        }

    @classmethod
    def generate_insights_report(
        cls,
        period: str = "week",
        browser: str = "chrome",
        format_type: str = "markdown",
    ) -> dict[str, Any]:
        """Generate comprehensive browsing insights report.

        Args:
            period: Time period - 'day', 'week', or 'month'
            browser: Browser to analyze
            format_type: 'markdown' for text or 'json' for data

        Returns:
            Dictionary with summary markdown and detailed data
        """
        from chronicle_mcp.core.categories import CATEGORY_DESCRIPTIONS

        browser_lower = validate_browser(browser)

        stats = cls._with_connection(browser_lower, db_get_browser_stats)
        productivity = cls.analyze_productivity(browser=browser_lower)
        top_domains = cls._with_connection(browser_lower, lambda conn: db_get_top_domains(conn, 5))

        insights_parts = [
            f"# Browsing Insights Report ({period})",
            f"\n**Browser:** {browser_lower}",
            f"\n**Total Visits:** {stats.get('total_visits', 0)}",
            f"\n**Unique URLs:** {stats.get('unique_urls', 0)}",
            "\n## Productivity",
            f"\n**Score:** {productivity['productivity_score']}/100 ({productivity['grade']}",
        ]

        for category, data in productivity.get("category_breakdown", {}).items():
            desc = CATEGORY_DESCRIPTIONS.get(category, category)
            insights_parts.append(
                f"- **{category.title()}** ({desc}): "
                f"{data.get('count', 0)} visits ({data.get('percentage', 0)}%)"
            )

        insights_parts.append("\n## Top Domains")
        for domain, count in top_domains:
            insights_parts.append(f"- {domain}: {count} visits")

        insights_parts.append("\n## Recommendations")
        for rec in productivity.get("recommendations", []):
            insights_parts.append(f"- {rec}")

        summary_markdown = "\n".join(insights_parts)

        if format_type == "json":
            return {
                "summary_markdown": summary_markdown,
                "data": {
                    "stats": stats,
                    "productivity": productivity,
                    "top_domains": top_domains,
                },
            }

        return {
            "summary_markdown": summary_markdown,
            "browser": browser_lower,
            "period": period,
        }

    @classmethod
    def subscribe_history_changes(
        cls,
        browser: str,
        event_types: list[str],
        callback: Callable[[Any], None] | None = None,
    ) -> dict[str, Any]:
        """Subscribe to history changes for a browser.

        Args:
            browser: Browser to subscribe to
            event_types: List of event types ('history_added', 'history_deleted', etc.)
            callback: Callback function to receive events

        Returns:
            Dictionary with subscription_id and stats
        """
        from chronicle_mcp.core.events import EventType
        from chronicle_mcp.core.realtime import get_subscription_manager

        browser_lower = validate_browser(browser)

        event_type_enums = []
        for et in event_types:
            try:
                event_type_enums.append(EventType(et))
            except ValueError:
                raise ValueError(f"Invalid event type: {et}")

        manager = get_subscription_manager()
        subscription_id = manager.subscribe(browser_lower, event_type_enums, callback if callback is not None else lambda e: None)
        stats = manager.get_stats()

        return {
            "subscription_id": subscription_id,
            "browser": browser_lower,
            "event_types": event_types,
            "active_subscriptions": stats.active_subscriptions,
            "total_events": stats.total_events,
        }

    @classmethod
    def unsubscribe_history_changes(cls, subscription_id: str) -> dict[str, Any]:
        """Unsubscribe from history changes.

        Args:
            subscription_id: Subscription ID to remove

        Returns:
            Dictionary with success status
        """
        from chronicle_mcp.core.realtime import get_subscription_manager

        manager = get_subscription_manager()
        success = manager.unsubscribe(subscription_id)

        return {
            "subscription_id": subscription_id,
            "success": success,
            "active_subscriptions": manager.get_active_count(),
        }

    @classmethod
    def get_subscription_status(cls, subscription_id: str | None = None) -> dict[str, Any]:
        """Get subscription status.

        Args:
            subscription_id: Optional specific subscription ID

        Returns:
            Dictionary with subscription info or global stats
        """
        from chronicle_mcp.core.realtime import get_subscription_manager

        manager = get_subscription_manager()

        if subscription_id:
            info = manager.get_subscription(subscription_id)
            if info:
                return {
                    "subscription_id": info.id,
                    "browser": info.browser,
                    "event_types": info.event_types,
                    "created_at": info.created_at,
                    "last_event": info.last_event,
                    "event_count": info.event_count,
                }
            return {"error": "Subscription not found"}

        stats = manager.get_stats()
        subscriptions = manager.get_subscriptions()

        return {
            "active_subscriptions": stats.active_subscriptions,
            "total_events": stats.total_events,
            "events_by_type": stats.events_by_type,
            "events_by_browser": stats.events_by_browser,
            "last_event_time": stats.last_event_time,
            "subscriptions": [
                {
                    "id": s.id,
                    "browser": s.browser,
                    "event_types": s.event_types,
                    "event_count": s.event_count,
                }
                for s in subscriptions
            ],
        }

    @classmethod
    def find_duplicate_entries(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        limit: int = 100,
    ) -> dict[str, Any]:
        """Find potential duplicate history entries.

        Args:
            browser: Browser to analyze
            similarity_threshold: URL similarity threshold (0.0-1.0)
            limit: Maximum number of duplicate groups to return

        Returns:
            Dictionary with duplicate groups and statistics
        """
        from difflib import SequenceMatcher

        browser_lower = validate_browser(browser)
        validate_limit(limit, 1, 1000)
        validate_fuzzy_threshold(similarity_threshold)

        def normalize_url_for_comparison(url: str) -> str:
            """Normalize URL for comparison (strip http/https, www, trailing slashes)."""
            url_clean = url.strip().lower()
            if url_clean.startswith("http://"):
                url_clean = url_clean[7:]
            elif url_clean.startswith("https://"):
                url_clean = url_clean[8:]
            if url_clean.startswith("www."):
                url_clean = url_clean[4:]
            url_clean = url_clean.rstrip("/")
            return url_clean

        def url_similarity(url1: str, url2: str) -> float:
            """Calculate similarity between two URLs."""
            url1_clean = normalize_url_for_comparison(url1)
            url2_clean = normalize_url_for_comparison(url2)
            if url1_clean == url2_clean:
                return 1.0
            return SequenceMatcher(None, url1_clean, url2_clean).ratio()

        duplicates: list[dict[str, Any]] = []
        seen_urls: list[tuple[str, str, int]] = []

        def get_entries(conn: Any) -> list[Any]:
            """Get history entries for comparison."""
            cursor = conn.cursor()
            schema = detect_schema(conn)
            if schema == "chrome":
                cursor.execute(
                    "SELECT title, url, visit_count FROM urls WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            elif schema == "firefox":
                cursor.execute(
                    "SELECT COALESCE(title, ''), url, visit_count FROM moz_places WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            elif schema == "safari":
                cursor.execute(
                    "SELECT title, url, visit_count FROM history_items WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT 500"
                )
            return cursor.fetchall()  # type: ignore[no-any-return]

        entries: list[tuple[str, str, int]] = cls._with_connection(browser_lower, get_entries)

        for url, title, visit_count in entries:
            if not url:
                continue
            url_duplicates: list[dict[str, Any]] = []
            for existing_url, existing_title, existing_count in seen_urls:
                sim = url_similarity(url, existing_url)
                if sim >= similarity_threshold:
                    url_duplicates.append(
                        {
                            "url": existing_url,
                            "title": existing_title,
                            "visit_count": existing_count,
                            "similarity": round(sim, 3),
                        }
                    )
            if url_duplicates:
                duplicates.append(
                    {
                        "url": url,
                        "title": title,
                        "visit_count": visit_count,
                        "similar_to": url_duplicates[:5],
                    }
                )
            seen_urls.append((url, title, visit_count))
            if len(duplicates) >= limit:
                break

        return {
            "browser": browser_lower,
            "similarity_threshold": similarity_threshold,
            "duplicate_groups": duplicates,
            "total_duplicates": len(duplicates),
            "total_entries_analyzed": len(entries),
        }

    @classmethod
    def delete_duplicates(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        keep_strategy: str = "most_visits",
        confirm: bool = False,
        _preview_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Delete duplicate history entries.

        Args:
            browser: Browser to clean
            similarity_threshold: URL similarity threshold for duplicates
            keep_strategy: Which entry to keep ('most_visits', 'most_recent', 'first')
            confirm: Must be True to actually delete; False returns preview
            _preview_result: Internal use - preview result from first call to avoid double computation

        Returns:
            Dictionary with deletion results or preview
        """
        browser_lower = validate_browser(browser)
        valid_strategies = ["most_visits", "most_recent", "first"]
        if keep_strategy not in valid_strategies:
            raise ValueError(f"Invalid keep_strategy. Must be one of: {valid_strategies}")

        if not confirm:
            preview_result = cls.find_duplicate_entries(
                browser=browser_lower,
                similarity_threshold=similarity_threshold,
                limit=100,
            )
            return {
                "preview": True,
                "message": f"Found {preview_result['total_duplicates']} duplicate groups",
                "duplicate_groups": preview_result["duplicate_groups"][:10],
                "total_duplicates": preview_result["total_duplicates"],
            }

        if _preview_result is None:
            preview_result = cls.find_duplicate_entries(
                browser=browser_lower,
                similarity_threshold=similarity_threshold,
                limit=100,
            )
        else:
            preview_result = _preview_result

        to_delete: list[tuple[str, str]] = []
        for group in preview_result["duplicate_groups"]:
            original_url = group["url"]
            for similar in group.get("similar_to", []):
                to_delete.append((similar["url"], original_url))

        if not to_delete:
            return {
                "preview": False,
                "deleted_count": 0,
                "total_pairs_checked": 0,
                "message": "No duplicate entries to delete",
            }

        def batch_delete(conn: Any) -> int:
            """Batch delete duplicate URLs using SQL IN clause with chunking."""
            cursor = conn.cursor()
            urls_to_delete = [url for url, _ in to_delete]
            if not urls_to_delete:
                return 0

            BATCH_SIZE = 500
            total_deleted = 0
            for i in range(0, len(urls_to_delete), BATCH_SIZE):
                batch = urls_to_delete[i : i + BATCH_SIZE]
                placeholders = ",".join("?" * len(batch))
                cursor.execute(f"DELETE FROM urls WHERE url IN ({placeholders})", batch)
                total_deleted += cursor.rowcount

            conn.commit()
            return total_deleted

        deleted_count = cls._with_connection(browser_lower, batch_delete)

        return {
            "preview": False,
            "deleted_count": deleted_count,
            "total_pairs_checked": len(to_delete),
            "message": f"Deleted {deleted_count} duplicate entries",
        }
