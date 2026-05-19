"""Database query operations for browser history.

This module provides functions for querying and manipulating browser history
across different browser schemas (Chrome, Firefox, Safari). It handles timestamp
conversion, URL sanitization, and schema-aware queries.
"""

import sqlite3
from datetime import datetime, timedelta, timezone

from chronicle_mcp.database.timestamps import (
    format_chrome_timestamp,
    format_firefox_timestamp,
    format_safari_timestamp,
)
from chronicle_mcp.database.utils import sanitize_url


def query_history(
    conn: sqlite3.Connection, query: str, limit: int = 10
) -> list[tuple[str, str, str]]:
    """
    Searches history for matching titles or URLs.

    Args:
        conn: SQLite connection
        query: Search term (supports LIKE wildcards)
        limit: Maximum results

    Returns:
        List of (title, url, timestamp) tuples
    """
    schema = detect_schema(conn)
    cols = get_schema_columns(schema)
    table = cols["table"]
    title_col = cols["title_col"]
    url_col = cols["url_col"]
    timestamp_col = cols["timestamp_col"]

    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute(
        f"SELECT {title_col}, {url_col}, {timestamp_col} FROM {table} WHERE {title_col} LIKE ? OR {url_col} LIKE ? ORDER BY {timestamp_col} DESC LIMIT ?",
        (search_query, search_query, limit),
    )
    results = cursor.fetchall()

    if schema == "chrome":
        return [
            (title, sanitize_url(url), format_chrome_timestamp(ts)) for title, url, ts in results
        ]
    elif schema == "firefox":
        return [
            (title, sanitize_url(url), format_firefox_timestamp(ts)) for title, url, ts in results
        ]
    else:
        return [
            (title, sanitize_url(url), format_safari_timestamp(ts)) for title, url, ts in results
        ]


def query_recent_history(
    conn: sqlite3.Connection, hours: int = 24, limit: int = 20
) -> list[tuple[str, str, str]]:
    """
    Gets recent history entries from the last N hours.

    Args:
        conn: SQLite connection
        hours: Number of hours to look back
        limit: Maximum results

    Returns:
        List of (title, url, timestamp) tuples
    """
    schema = detect_schema(conn)
    cols = get_schema_columns(schema)
    table = cols["table"]
    title_col = cols["title_col"]
    url_col = cols["url_col"]
    timestamp_col = cols["timestamp_col"]

    if schema == "chrome":
        chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    elif schema == "firefox":
        chrome_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    else:
        chrome_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    cutoff_timestamp = int((cutoff - chrome_epoch).total_seconds() * 1_000_000)

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {title_col}, {url_col}, {timestamp_col} FROM {table} WHERE {timestamp_col} > ? ORDER BY {timestamp_col} DESC LIMIT ?",
        (cutoff_timestamp, limit),
    )
    results = cursor.fetchall()

    if schema == "chrome":
        return [
            (title, sanitize_url(url), format_chrome_timestamp(ts)) for title, url, ts in results
        ]
    elif schema == "firefox":
        return [
            (title, sanitize_url(url), format_firefox_timestamp(ts)) for title, url, ts in results
        ]
    else:
        return [
            (title, sanitize_url(url), format_safari_timestamp(ts)) for title, url, ts in results
        ]


def count_domain_visits(conn: sqlite3.Connection, domain: str) -> int:
    """
    Counts visits to a specific domain.

    Args:
        conn: SQLite connection
        domain: Domain to count (e.g., 'github.com')

    Returns:
        Number of visits to the domain
    """
    schema = detect_schema(conn)
    cols = get_schema_columns(schema)
    table = cols["table"]
    url_col = cols["url_col"]
    visit_count_col = cols["visit_count_col"]

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT SUM({visit_count_col}) FROM {table} WHERE {url_col} LIKE ?",
        (f"%://{domain}/%",),
    )
    result = cursor.fetchone()
    return int(result[0]) if result and result[0] else 0


def get_top_domains(conn: sqlite3.Connection, limit: int = 10) -> list[tuple[str, int]]:
    """
    Gets most visited domains.

    Args:
        conn: SQLite connection
        limit: Maximum number of domains to return

    Returns:
        List of (domain, visit_count) tuples
    """
    schema = detect_schema(conn)

    if schema == "firefox":
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT SUBSTR(
                SUBSTR(p.url, INSTR(p.url, '://') + 3),
                1,
                CASE
                    WHEN INSTR(SUBSTR(p.url, INSTR(p.url, '://') + 3), '/') > 0
                    THEN INSTR(SUBSTR(p.url, INSTR(p.url, '://') + 3), '/') - 1
                    ELSE 100
                END
            ) as domain, SUM(p.visit_count) as total
            FROM moz_places p
            WHERE p.visit_count > 0 AND p.url LIKE 'http%'
            GROUP BY domain
            ORDER BY total DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [(row[0], row[1]) for row in cursor.fetchall()]

    if schema != "chrome":
        return []

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT SUBSTR(
            SUBSTR(url, INSTR(url, '://') + 3),
            1,
            CASE
                WHEN INSTR(SUBSTR(url, INSTR(url, '://') + 3), '/') > 0
                THEN INSTR(SUBSTR(url, INSTR(url, '://') + 3), '/') - 1
                ELSE 100
            END
        ) as domain, SUM(visit_count) as total
        FROM urls
        WHERE url LIKE 'http%' OR url LIKE 'https%'
        GROUP BY domain
        ORDER BY total DESC
        LIMIT ?
    """,
        (limit,),
    )
    return [(row[0], row[1]) for row in cursor.fetchall()]


def search_by_date(
    conn: sqlite3.Connection, query: str, start_date: str, end_date: str, limit: int = 10
) -> list[tuple[str, str, str]]:
    """
    Searches history within a date range.

    Args:
        conn: SQLite connection
        query: Search term
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        limit: Maximum results

    Returns:
        List of (title, url, timestamp) tuples
    """
    from datetime import datetime, timezone

    schema = detect_schema(conn)
    cols = get_schema_columns(schema)
    table = cols["table"]
    title_col = cols["title_col"]
    url_col = cols["url_col"]
    timestamp_col = cols["timestamp_col"]

    if schema == "chrome":
        epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    elif schema == "firefox":
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    else:
        epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)

    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)

        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)

        start_microseconds = int((start_dt - epoch).total_seconds() * 1_000_000)
        end_microseconds = int((end_dt - epoch).total_seconds() * 1_000_000)
    except ValueError:
        return []

    search_query = f"%{query}%"
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT {title_col}, {url_col}, {timestamp_col} FROM {table}
           WHERE ({title_col} LIKE ? OR {url_col} LIKE ?)
           AND {timestamp_col} >= ? AND {timestamp_col} <= ?
           ORDER BY {timestamp_col} DESC LIMIT ?""",
        (search_query, search_query, start_microseconds, end_microseconds, limit),
    )
    results = cursor.fetchall()

    if schema == "chrome":
        return [
            (title, sanitize_url(url), format_chrome_timestamp(ts)) for title, url, ts in results
        ]
    elif schema == "firefox":
        return [
            (title, sanitize_url(url), format_firefox_timestamp(ts)) for title, url, ts in results
        ]
    else:
        return [
            (title, sanitize_url(url), format_safari_timestamp(ts)) for title, url, ts in results
        ]


def format_results(
    rows: list[tuple[str, str, str]], query: str, format_type: str = "markdown"
) -> str:
    """
    Formats history results for output.

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
        import json

        items = [
            {"title": title, "url": sanitize_url(url), "timestamp": ts} for title, url, ts in rows
        ]
        return json.dumps({"results": items, "count": len(items)})

    results = [
        f"- **{title}**\n  URL: {sanitize_url(url)}\n  Timestamp: {ts}" for title, url, ts in rows
    ]
    return "\n\n".join(results)


def delete_history(conn: sqlite3.Connection, query: str, limit: int = 100) -> int:
    """
    Deletes history entries matching a query.

    Args:
        conn: SQLite connection
        query: Search term to match for deletion
        limit: Maximum number of entries to delete

    Returns:
        Number of entries deleted
    """
    schema = detect_schema(conn)
    cols = get_schema_columns(schema)
    table = cols["table"]
    title_col = cols["title_col"]
    url_col = cols["url_col"]
    timestamp_col = cols["timestamp_col"]

    cursor = conn.cursor()
    search_query = f"%{query}%"

    if schema == "firefox":
        cursor.execute(
            f"""DELETE FROM {table} WHERE rowid IN (
                SELECT p.rowid FROM {table} p
                WHERE (p.{title_col} LIKE ? OR p.{url_col} LIKE ?)
                ORDER BY p.{timestamp_col} DESC LIMIT ?
            )""",
            (search_query, search_query, limit),
        )
    else:
        cursor.execute(
            f"""DELETE FROM {table} WHERE (title LIKE ? OR url LIKE ?) AND rowid IN (
                SELECT rowid FROM {table} WHERE (title LIKE ? OR url LIKE ?)
                ORDER BY {timestamp_col} DESC LIMIT ?
            )""",
            (search_query, search_query, search_query, search_query, limit),
        )

    deleted_count = cursor.rowcount
    conn.commit()
    return deleted_count if deleted_count > 0 else 0


def detect_schema(conn: sqlite3.Connection) -> str:
    """
    Detects the browser database schema type.

    Args:
        conn: SQLite connection

    Returns:
        Schema type: 'chrome', 'firefox', or 'safari'
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    if "urls" in tables:
        return "chrome"
    elif "moz_places" in tables:
        return "firefox"
    elif "history_items" in tables:
        return "safari"
    else:
        return "unknown"


SCHEMA_COLUMNS: dict[str, dict[str, str]] = {
    "chrome": {
        "table": "urls",
        "title_col": "title",
        "url_col": "url",
        "timestamp_col": "last_visit_time",
        "visit_count_col": "visit_count",
    },
    "firefox": {
        "table": "moz_places",
        "title_col": "title",
        "url_col": "url",
        "timestamp_col": "last_visit_date",
        "visit_count_col": "visit_count",
    },
    "safari": {
        "table": "history_items",
        "title_col": "title",
        "url_col": "url",
        "timestamp_col": "visit_time",
        "visit_count_col": "visit_count",
    },
}


def get_schema_columns(schema: str) -> dict[str, str]:
    """Get column/table mapping for a schema."""
    return SCHEMA_COLUMNS.get(schema, SCHEMA_COLUMNS["chrome"])
