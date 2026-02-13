"""Response formatting functions for ChronicleMCP service layer.

This module provides pure functions to format structured data
into various output formats (markdown, JSON, CSV).
"""

import csv
import json
from io import StringIO
from typing import Any


def format_search_results(
    rows: list[tuple[str, str, str]],
    query: str,
    format_type: str = "markdown"
) -> str:
    """Format search results for output.

    Args:
        rows: List of (title, url, timestamp) tuples
        query: Original search query (for 'not found' message)
        format_type: 'markdown' or 'json'

    Returns:
        Formatted string output
    """
    if not rows:
        return f"No history found for: {query}"

    if format_type == "json":
        items = [
            {"title": title, "url": url, "timestamp": ts}
            for title, url, ts in rows
        ]
        return json.dumps({"results": items, "count": len(items)})

    # Markdown format
    results = [
        f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}"
        for title, url, ts in rows
    ]
    return "\n\n".join(results)


def format_recent_results(
    rows: list[tuple[str, str, str]],
    hours: int,
    format_type: str = "markdown"
) -> str:
    """Format recent history results for output.

    Args:
        rows: List of (title, url, timestamp) tuples
        hours: Number of hours queried
        format_type: 'markdown' or 'json'

    Returns:
        Formatted string output
    """
    if format_type == "json":
        items = [
            {"title": title, "url": url, "timestamp": ts}
            for title, url, ts in rows
        ]
        return json.dumps({"results": items, "count": len(items)})

    if not rows:
        return f"No history found in the last {hours} hours"

    # Markdown format
    results = [
        f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}"
        for title, url, ts in rows
    ]
    return f"History from last {hours} hours:\n\n" + "\n\n".join(results)


def format_domain_visits(domain: str, browser: str, count: int) -> str:
    """Format domain visit count.

    Args:
        domain: Domain name
        browser: Browser name
        count: Visit count

    Returns:
        Formatted string
    """
    return f"Visits to '{domain}' in {browser}: {count}"


def format_top_domains(
    domains: list[tuple[str, int]],
    format_type: str = "markdown"
) -> str:
    """Format top domains list.

    Args:
        domains: List of (domain, visits) tuples
        format_type: 'markdown' or 'json'

    Returns:
        Formatted string output
    """
    if format_type == "json":
        return json.dumps({
            "top_domains": [{"domain": d, "visits": v} for d, v in domains]
        })

    if not domains:
        return "No domain data found"

    # Markdown format
    results = [f"- **{domain}** ({visits} visits)" for domain, visits in domains]
    return "\n\n".join(results)


def format_most_visited_pages(
    pages: list[tuple[str, str, int]],
    format_type: str = "markdown"
) -> str:
    """Format most visited pages list.

    Args:
        pages: List of (title, url, visits) tuples
        format_type: 'markdown' or 'json'

    Returns:
        Formatted string output
    """
    if format_type == "json":
        return json.dumps({
            "top_pages": [
                {"title": title, "url": url, "visits": visits}
                for title, url, visits in pages
            ]
        })

    if not pages:
        return "No page data found"

    # Markdown format
    results = [
        f"- **{title}**\n  URL: {url}\n  Visits: {visits}"
        for title, url, visits in pages
    ]
    return "Most visited pages:\n\n" + "\n\n".join(results)


def format_domain_search_results(
    rows: list[tuple[str, str, str]],
    domain: str,
    query: str | None,
    format_type: str = "markdown"
) -> str:
    """Format domain-specific search results.

    Args:
        rows: List of (title, url, timestamp) tuples
        domain: Domain searched
        query: Optional search query within domain
        format_type: 'markdown' or 'json'

    Returns:
        Formatted string output
    """
    if format_type == "json":
        return json.dumps({
            "domain": domain,
            "results": [
                {"title": title, "url": url, "timestamp": ts}
                for title, url, ts in rows
            ],
            "count": len(rows),
        })

    if not rows:
        return f"No history found for domain: {domain}"

    # Markdown format
    search_desc = f"'{query}' in {domain}" if query else domain
    results = [
        f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}"
        for title, url, ts in rows
    ]
    return f"History for {search_desc}:\n\n" + "\n\n".join(results)


def format_advanced_search_results(
    rows: list[tuple[str, str, str]],
    query: str,
    format_type: str = "markdown",
    options: dict[str, Any] | None = None
) -> str:
    """Format advanced search results.

    Args:
        rows: List of (title, url, timestamp) tuples
        query: Search query
        format_type: 'markdown' or 'json'
        options: Search options used

    Returns:
        Formatted string output
    """
    if format_type == "json":
        return json.dumps({
            "query": query,
            "results": [
                {"title": title, "url": url, "timestamp": ts}
                for title, url, ts in rows
            ],
            "count": len(rows),
            "options": options or {}
        })

    if not rows:
        return f"No history found for: {query}"

    # Markdown format
    results = [
        f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}"
        for title, url, ts in rows
    ]
    return "\n\n".join(results)


def format_browser_stats(stats: dict[str, Any]) -> str:
    """Format browser statistics as JSON.

    Args:
        stats: Dictionary with browser statistics

    Returns:
        JSON formatted string
    """
    return json.dumps(stats, indent=2)


def format_export(
    rows: list[dict[str, Any]],
    format_type: str = "csv"
) -> str:
    """Format data for export.

    Args:
        rows: List of dictionaries with title, url, timestamp
        format_type: 'csv' or 'json'

    Returns:
        Formatted export string
    """
    if format_type == "csv":
        output = StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=["title", "url", "timestamp"])
            writer.writeheader()
            writer.writerows(rows)
        return output.getvalue()

    elif format_type == "json":
        return json.dumps({"exported_entries": len(rows), "entries": rows}, indent=2)

    else:
        raise ValueError(f"Unsupported export format: {format_type}")


def format_delete_preview(query: str, count: int) -> str:
    """Format delete preview message.

    Args:
        query: Search query that would be deleted
        count: Number of entries that would be deleted

    Returns:
        Preview message string
    """
    return (
        f"Permanent delete preview: {count} entries would be deleted "
        f"matching '{query}'. Set confirm=true to execute."
    )


def format_delete_result(query: str, browser: str, count: int) -> str:
    """Format delete success message.

    Args:
        query: Search query that was deleted
        browser: Browser name
        count: Number of entries deleted

    Returns:
        Success message string
    """
    return f"Deleted {count} history entries matching '{query}' from {browser}"


def format_sync_preview(
    source: str,
    target: str,
    entries_count: int,
    merge_strategy: str
) -> str:
    """Format sync dry-run preview message.

    Args:
        source: Source browser
        target: Target browser
        entries_count: Number of entries to sync
        merge_strategy: Merge strategy name

    Returns:
        Preview message string
    """
    return (
        f"Dry run: Would sync {entries_count} entries from {source} to {target} "
        f"using '{merge_strategy}' strategy"
    )


def format_sync_result(
    source: str,
    target: str,
    entries_count: int,
    merge_strategy: str
) -> str:
    """Format sync success message.

    Args:
        source: Source browser
        target: Target browser
        entries_count: Number of entries synced
        merge_strategy: Merge strategy name

    Returns:
        Success message string
    """
    return (
        f"Synced {entries_count} entries from {source} to {target} "
        f"using '{merge_strategy}' strategy"
    )


def format_available_browsers(browsers: list[str]) -> str:
    """Format available browsers list.

    Args:
        browsers: List of available browser names

    Returns:
        Formatted string
    """
    if not browsers:
        return "No browsers with history found on this system"

    return f"Available browsers: {', '.join(browsers)}"


def format_error_message(message: str) -> str:
    """Format error message for MCP protocol.

    Args:
        message: Error message

    Returns:
        Formatted error string
    """
    return f"Error: {message}"
