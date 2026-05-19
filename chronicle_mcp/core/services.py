"""Facade service layer for ChronicleMCP.

This module provides the main HistoryService class that delegates to
specialized service modules for different functionality areas.
"""

from typing import Any

from chronicle_mcp.core import (
    analytics_service,
    bookmarks_service,
    browser_service,
    dedup_service,
    domain_service,
    history_service,
    search_service,
    subscription_service,
)
from chronicle_mcp.core._connection import with_connection


class HistoryService:
    """Facade service that delegates to specialized service modules."""

    _with_connection = staticmethod(with_connection)

    @classmethod
    def list_available_browsers(cls) -> dict[str, Any]:
        return browser_service.list_available_browsers()

    @classmethod
    def search_history(
        cls, query: str, limit: int = 5, browser: str = "chrome", format_type: str = "markdown"
    ) -> dict[str, Any]:
        return search_service.search_history(query, limit, browser, format_type)

    @classmethod
    def get_recent_history(
        cls,
        hours: int = 24,
        limit: int = 20,
        browser: str = "chrome",
        format_type: str = "markdown",
    ) -> dict[str, Any]:
        return search_service.get_recent_history(hours, limit, browser, format_type)

    @classmethod
    def count_visits(cls, domain: str, browser: str = "chrome") -> dict[str, Any]:
        return search_service.count_visits(domain, browser)

    @classmethod
    def list_top_domains(
        cls, limit: int = 10, browser: str = "chrome", format_type: str = "markdown"
    ) -> dict[str, Any]:
        return search_service.list_top_domains(limit, browser, format_type)

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
        return search_service.search_history_by_date(
            query, start_date, end_date, limit, browser, format_type
        )

    @classmethod
    def delete_history(
        cls, query: str, limit: int = 100, browser: str = "chrome", confirm: bool = False
    ) -> dict[str, Any]:
        return history_service.delete_history(query, limit, browser, confirm)

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
        return domain_service.search_by_domain(
            domain, query, limit, browser, format_type, exclude_domains
        )

    @classmethod
    def get_browser_stats(
        cls, browser: str = "chrome", format_type: str = "markdown"
    ) -> dict[str, Any]:
        return analytics_service.get_browser_stats(browser, format_type)

    @classmethod
    def get_most_visited_pages(
        cls, limit: int = 20, browser: str = "chrome", format_type: str = "markdown"
    ) -> dict[str, Any]:
        return search_service.get_most_visited_pages(limit, browser, format_type)

    @classmethod
    def export_history(
        cls,
        format_type: str = "csv",
        limit: int = 1000,
        query: str | None = None,
        browser: str = "chrome",
    ) -> dict[str, Any]:
        return history_service.export_history(format_type, limit, query, browser)

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
        return search_service.search_history_advanced(
            query,
            limit,
            browser,
            format_type,
            exclude_domains,
            sort_by,
            use_regex,
            use_fuzzy,
            fuzzy_threshold,
        )

    @classmethod
    def sync_history(
        cls,
        source_browser: str,
        target_browser: str,
        merge_strategy: str = "latest",
        dry_run: bool = True,
    ) -> dict[str, Any]:
        return history_service.sync_history(source_browser, target_browser, merge_strategy, dry_run)

    @classmethod
    def list_available_bookmarks(cls) -> dict[str, Any]:
        return browser_service.list_available_bookmarks()

    @classmethod
    def list_available_downloads(cls) -> dict[str, Any]:
        return browser_service.list_available_downloads()

    @classmethod
    def get_bookmarks(
        cls,
        query: str | None = None,
        limit: int = 50,
        browser: str = "chrome",
        format_type: str = "markdown",
    ) -> dict[str, Any]:
        return bookmarks_service.get_bookmarks(query, limit, browser, format_type)

    @classmethod
    def get_downloads(
        cls,
        query: str | None = None,
        limit: int = 50,
        browser: str = "chrome",
        format_type: str = "markdown",
    ) -> dict[str, Any]:
        return bookmarks_service.get_downloads(query, limit, browser, format_type)

    @classmethod
    def compare_time_periods(
        cls,
        start_date1: str,
        end_date1: str,
        start_date2: str,
        end_date2: str,
        browser: str = "chrome",
    ) -> dict[str, Any]:
        return analytics_service.compare_time_periods(
            start_date1, end_date1, start_date2, end_date2, browser
        )

    @classmethod
    def analyze_productivity(
        cls,
        start_date: str | None = None,
        end_date: str | None = None,
        browser: str = "chrome",
    ) -> dict[str, Any]:
        return analytics_service.analyze_productivity(start_date, end_date, browser)

    @classmethod
    def suggest_categories(
        cls,
        browser: str = "chrome",
        limit: int = 20,
    ) -> dict[str, Any]:
        return analytics_service.suggest_categories(browser, limit)

    @classmethod
    def export_visualization(
        cls,
        format_type: str = "chart_json",
        period: str = "month",
        browser: str = "chrome",
    ) -> dict[str, Any]:
        return analytics_service.export_visualization(format_type, period, browser)

    @classmethod
    def generate_insights_report(
        cls,
        period: str = "week",
        browser: str = "chrome",
        format_type: str = "markdown",
    ) -> dict[str, Any]:
        return analytics_service.generate_insights_report(period, browser, format_type)

    @classmethod
    def subscribe_history_changes(
        cls,
        browser: str,
        event_types: list[str],
        callback: Any = None,
    ) -> dict[str, Any]:
        return subscription_service.SubscriptionService.subscribe_history_changes(
            browser, event_types, callback
        )

    @classmethod
    def unsubscribe_history_changes(cls, subscription_id: str) -> dict[str, Any]:
        return subscription_service.SubscriptionService.unsubscribe_history_changes(subscription_id)

    @classmethod
    def get_subscription_status(cls, subscription_id: str | None = None) -> dict[str, Any]:
        return subscription_service.SubscriptionService.get_subscription_status(subscription_id)

    @classmethod
    def find_duplicate_entries(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        limit: int = 100,
    ) -> dict[str, Any]:
        return dedup_service.DedupService.find_duplicate_entries(
            browser, similarity_threshold, limit
        )

    @classmethod
    def delete_duplicates(
        cls,
        browser: str,
        similarity_threshold: float = 0.9,
        keep_strategy: str = "most_visits",
        confirm: bool = False,
        _preview_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return dedup_service.DedupService.delete_duplicates(
            browser, similarity_threshold, keep_strategy, confirm, _preview_result
        )
