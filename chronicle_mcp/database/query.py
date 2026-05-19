"""Database query module - re-exports from specialized modules.

This module re-exports all functions from the specialized database modules
for backwards compatibility.
"""

from chronicle_mcp.database.analytics_helpers import (
    get_category_stats,
    get_hourly_stats_for_period,
    get_uncategorized_urls,
    get_visit_patterns_by_hour,
    search_history_for_period,
)
from chronicle_mcp.database.bookmarks import (
    query_bookmarks,
    query_bookmarks_chrome,
    query_bookmarks_firefox,
    query_downloads,
    query_downloads_chrome,
    query_downloads_firefox,
)
from chronicle_mcp.database.history_queries import (
    SCHEMA_COLUMNS,
    count_domain_visits,
    delete_history,
    detect_schema,
    format_results,
    get_schema_columns,
    get_top_domains,
    query_history,
    query_recent_history,
    search_by_date,
)
from chronicle_mcp.database.search_advanced import (
    export_history,
    get_browser_stats,
    get_history_entries,
    get_most_visited_pages,
    insert_history_entries,
    query_history_universal,
    search_by_domain,
    search_history_advanced,
    search_with_fuzzy,
    search_with_regex,
    sync_to_browser,
)

__all__ = [
    "SCHEMA_COLUMNS",
    "count_domain_visits",
    "delete_history",
    "detect_schema",
    "export_history",
    "format_results",
    "get_browser_stats",
    "get_category_stats",
    "get_history_entries",
    "get_hourly_stats_for_period",
    "get_most_visited_pages",
    "get_schema_columns",
    "get_top_domains",
    "get_uncategorized_urls",
    "get_visit_patterns_by_hour",
    "insert_history_entries",
    "query_bookmarks",
    "query_bookmarks_chrome",
    "query_bookmarks_firefox",
    "query_downloads",
    "query_downloads_chrome",
    "query_downloads_firefox",
    "query_history",
    "query_history_universal",
    "query_recent_history",
    "search_by_date",
    "search_by_domain",
    "search_history_advanced",
    "search_history_for_period",
    "search_with_fuzzy",
    "search_with_regex",
    "sync_to_browser",
]
