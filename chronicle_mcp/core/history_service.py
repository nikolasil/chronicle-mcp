"""History service for delete, sync, and export operations."""

import json
from typing import Any

from chronicle_mcp.core._connection import with_connection
from chronicle_mcp.core.exceptions import BrowserNotFoundError
from chronicle_mcp.core.formatters import (
    format_delete_preview,
    format_delete_result,
    format_sync_preview,
    format_sync_result,
)
from chronicle_mcp.core.validation import (
    validate_browser,
    validate_browsers_different,
    validate_format_type,
    validate_limit,
    validate_merge_strategy,
    validate_query,
)
from chronicle_mcp.database import (
    delete_history as db_delete_history,
)
from chronicle_mcp.database import (
    export_history as db_export_history,
)
from chronicle_mcp.database import (
    get_history_entries,
    query_history,
    sync_to_browser,
)
from chronicle_mcp.paths import get_browser_path


def delete_history(
    query: str, limit: int = 100, browser: str = "chrome", confirm: bool = False
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
        rows = with_connection(
            browser_lower, lambda conn: query_history(conn, query_clean, limit_val)
        )
        count = len(rows)

        return {
            "preview": True,
            "query": query_clean,
            "count": count,
            "message": format_delete_preview(query_clean, count),
        }

    deleted = with_connection(
        browser_lower, lambda conn: db_delete_history(conn, query_clean, limit_val)
    )

    return {
        "deleted": deleted,
        "query": query_clean,
        "browser": browser_lower,
        "message": format_delete_result(query_clean, browser_lower, deleted),
    }


def sync_history(
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

    source_path = get_browser_path(source)
    target_path = get_browser_path(target)

    if not source_path:
        raise BrowserNotFoundError(source)

    if not target_path:
        raise BrowserNotFoundError(target)

    entries_json = with_connection(source, lambda conn: db_export_history(conn, "json", 10000))
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

    entries = with_connection(source, lambda conn: get_history_entries(conn, 10000))

    synced_count = sync_to_browser(target_path, entries, strategy)

    return {
        "dry_run": False,
        "source": source,
        "target": target,
        "entries_count": synced_count,
        "merge_strategy": strategy,
        "message": format_sync_result(source, target, synced_count, strategy),
    }


def export_history(
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

    content = with_connection(
        browser_lower, lambda conn: db_export_history(conn, format_clean, limit_val, query)
    )

    return {"content": content, "format": format_clean, "browser": browser_lower}
