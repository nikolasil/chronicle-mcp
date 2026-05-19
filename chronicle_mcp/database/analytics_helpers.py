"""Analytics helper functions for browser history analysis.

This module provides functions for analyzing browsing patterns,
category statistics, and time-based analytics.
"""

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

from chronicle_mcp.database.timestamps import format_chrome_timestamp
from chronicle_mcp.database.utils import sanitize_url


def get_category_stats(
    conn: sqlite3.Connection,
    category_domains: dict[str, list[str]],
) -> dict[str, int]:
    """
    Gets visit counts per category based on domain matching.

    Args:
        conn: SQLite connection
        category_domains: Dict mapping category to list of domain patterns

    Returns:
        Dict mapping category to visit count
    """
    cursor = conn.cursor()
    category_counts: dict[str, int] = {}

    for category, domains in category_domains.items():
        if not domains:
            category_counts[category] = 0
            continue

        sql = f"""
            SELECT COALESCE(SUM(visit_count), 0) as total
            FROM urls
            WHERE {" OR ".join(["url LIKE ?" for _ in domains])}
        """
        params: list[str] = [f"%{d}%" for d in domains]

        cursor.execute(sql, params)
        result = cursor.fetchone()
        category_counts[category] = result[0] if result else 0

    uncategorized_count = _get_uncategorized_count(conn, category_domains)
    category_counts["uncategorized"] = uncategorized_count

    return category_counts


def _get_uncategorized_count(
    conn: sqlite3.Connection,
    category_domains: dict[str, list[str]],
) -> int:
    """Count visits that don't match any known category."""
    cursor = conn.cursor()

    all_known_domains: list[str] = []
    for domains in category_domains.values():
        all_known_domains.extend(domains)

    if not all_known_domains:
        cursor.execute("SELECT COALESCE(SUM(visit_count), 0) FROM urls")
        result = cursor.fetchone()
        return result[0] if result else 0

    exclude_conditions = " OR ".join(["url LIKE ?" for _ in all_known_domains])
    params = [f"%{d}%" for d in all_known_domains]

    sql = f"""
        SELECT COALESCE(SUM(visit_count), 0) as total
        FROM urls
        WHERE NOT ({exclude_conditions})
    """

    cursor.execute(sql, params)
    result = cursor.fetchone()
    return result[0] if result else 0


def get_visit_patterns_by_hour(conn: sqlite3.Connection) -> dict[int, int]:
    """
    Gets visit distribution by hour of day.

    Args:
        conn: SQLite connection

    Returns:
        Dict mapping hour (0-23) to visit count
    """
    cursor = conn.cursor()
    cursor.execute("SELECT last_visit_time FROM urls WHERE last_visit_time > 0")

    hour_counts: dict[int, int] = {h: 0 for h in range(24)}

    for (timestamp,) in cursor.fetchall():
        try:
            epoch_delta = timedelta(microseconds=timestamp)
            chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
            dt = chrome_epoch + epoch_delta
            hour_counts[dt.hour] += 1
        except (ValueError, OverflowError):
            continue

    return hour_counts


def search_history_for_period(
    conn: sqlite3.Connection,
    start_date: str,
    end_date: str,
) -> list[tuple[str, str, str]]:
    """
    Gets history entries within a date range.

    Args:
        conn: SQLite connection
        start_date: Start date ISO format
        end_date: End date ISO format

    Returns:
        List of (title, url, timestamp) tuples
    """
    cursor = conn.cursor()

    try:
        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    except ValueError:
        return []

    chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    start_microseconds = int((start_dt - chrome_epoch).total_seconds() * 1000000)
    end_microseconds = int((end_dt - chrome_epoch).total_seconds() * 1000000)

    cursor.execute(
        """
        SELECT title, url, last_visit_time
        FROM urls
        WHERE last_visit_time >= ? AND last_visit_time <= ?
        ORDER BY last_visit_time DESC
        """,
        (start_microseconds, end_microseconds),
    )

    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
    ]


def get_hourly_stats_for_period(
    conn: sqlite3.Connection,
    start_date: str,
    end_date: str,
) -> dict[str, Any]:
    """
        Gets statistics for a specific time period.

        Args:
            conn: SQLite connection
            start_date: Start date ISO format
            end_date: End date ISO format

    Returns:
            List of (title, url, timestamp) tuples
    """
    cursor = conn.cursor()

    try:
        start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
    except ValueError:
        return {"total_visits": 0, "unique_urls": 0, "top_domains": []}

    chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=timezone.utc)
    start_microseconds = int((start_dt - chrome_epoch).total_seconds() * 1000000)
    end_microseconds = int((end_dt - chrome_epoch).total_seconds() * 1000000)

    cursor.execute(
        """
        SELECT COUNT(*), COALESCE(SUM(visit_count), 0),
               COUNT(DISTINCT url)
        FROM urls
        WHERE last_visit_time >= ? AND last_visit_time <= ?
        """,
        (start_microseconds, end_microseconds),
    )
    count_row = cursor.fetchone()
    total_entries = count_row[0] if count_row else 0
    total_visits = count_row[1] if count_row else 0
    unique_urls = count_row[2] if count_row else 0

    cursor.execute(
        """
        SELECT COUNT(*) as cnt,
               SUBSTR(
                   SUBSTR(url, INSTR(url, '://') + 3),
                   1,
                   CASE
                       WHEN INSTR(SUBSTR(url, INSTR(url, '://') + 3), '/') > 0
                       THEN INSTR(SUBSTR(url, INSTR(url, '://') + 3), '/') - 1
                       ELSE 100
                   END
               ) as domain
        FROM urls
        WHERE last_visit_time >= ? AND last_visit_time <= ?
        GROUP BY domain
        ORDER BY cnt DESC
        LIMIT 10
        """,
        (start_microseconds, end_microseconds),
    )
    top_domains = [(row[1], row[0]) for row in cursor.fetchall()]

    return {
        "total_entries": total_entries,
        "total_visits": total_visits,
        "unique_urls": unique_urls,
        "top_domains": top_domains,
    }


def get_uncategorized_urls(
    conn: sqlite3.Connection,
    category_domains: dict[str, list[str]],
    limit: int = 20,
) -> list[tuple[str, str, int]]:
    """
    Gets URLs that don't match any known category.

    Args:
        conn: SQLite connection
        category_domains: Dict mapping category to list of domain patterns
        limit: Maximum results

    Returns:
        List of (title, url, visit_count) tuples
    """
    cursor = conn.cursor()

    all_known_domains: list[str] = []
    for domains in category_domains.values():
        all_known_domains.extend(domains)

    if not all_known_domains:
        cursor.execute(
            """
            SELECT title, url, visit_count
            FROM urls
            WHERE title IS NOT NULL
            ORDER BY visit_count DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [(row[0], sanitize_url(row[1]), row[2]) for row in cursor.fetchall()]

    exclude_conditions = " OR ".join(["url LIKE ?" for _ in all_known_domains])
    params: list[str | int] = [f"%{d}%" for d in all_known_domains]
    params.append(limit)

    sql = f"""
        SELECT title, url, visit_count
        FROM urls
        WHERE NOT ({exclude_conditions})
        AND title IS NOT NULL
        ORDER BY visit_count DESC
        LIMIT ?
    """

    cursor.execute(sql, params)
    return [(row[0], sanitize_url(row[1]), row[2]) for row in cursor.fetchall()]
