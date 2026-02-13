"""Core business logic layer for ChronicleMCP.

This package provides the service layer that handles all business logic,
validation, and formatting. Protocol adapters (MCP, HTTP) consume these
services to provide their respective interfaces.
"""

from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    BrowserPathNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    InvalidDateRangeError,
    PermissionDeniedError,
    ServiceError,
    UnsupportedFormatError,
    ValidationError,
)
from chronicle_mcp.core.formatters import (
    format_advanced_search_results,
    format_available_browsers,
    format_browser_stats,
    format_delete_preview,
    format_delete_result,
    format_domain_search_results,
    format_domain_visits,
    format_error_message,
    format_export,
    format_most_visited_pages,
    format_recent_results,
    format_search_results,
    format_sync_preview,
    format_sync_result,
    format_top_domains,
)
from chronicle_mcp.core.services import HistoryService
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

__all__ = [
    # Service
    "HistoryService",
    # Exceptions
    "ServiceError",
    "ValidationError",
    "BrowserNotFoundError",
    "BrowserPathNotFoundError",
    "DatabaseLockedError",
    "PermissionDeniedError",
    "DatabaseError",
    "UnsupportedFormatError",
    "InvalidDateRangeError",
    # Validation
    "validate_browser",
    "validate_query",
    "validate_limit",
    "validate_hours",
    "validate_format_type",
    "validate_domain",
    "validate_date_range",
    "validate_sort_by",
    "validate_fuzzy_threshold",
    "validate_search_options",
    "validate_merge_strategy",
    "validate_browsers_different",
    "validate_exclude_domains",
    # Formatters
    "format_search_results",
    "format_recent_results",
    "format_domain_visits",
    "format_top_domains",
    "format_most_visited_pages",
    "format_domain_search_results",
    "format_advanced_search_results",
    "format_browser_stats",
    "format_export",
    "format_delete_preview",
    "format_delete_result",
    "format_sync_preview",
    "format_sync_result",
    "format_available_browsers",
    "format_error_message",
]
