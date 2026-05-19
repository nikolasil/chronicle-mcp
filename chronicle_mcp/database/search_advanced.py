"""Advanced search operations for browser history.

This module provides advanced search capabilities including domain filtering,
regex search, fuzzy matching, and multi-option search.
"""

import re
import sqlite3
import threading
from typing import Any

from chronicle_mcp.database.sql_builder import build_search_query
from chronicle_mcp.database.timestamps import (
    format_chrome_timestamp,
    format_firefox_timestamp,
    format_safari_timestamp,
)
from chronicle_mcp.database.utils import fuzzy_match_score, sanitize_url


def search_by_domain(
    conn: sqlite3.Connection,
    domain: str,
    query: str | None = None,
    limit: int = 20,
    exclude_domains: list[str] | None = None,
) -> list[tuple[str, str, str]]:
    """
    Searches history within specific domain(s).

    Args:
        conn: SQLite connection
        domain: Domain to search within (e.g., 'github.com')
        query: Optional search term within the domain
        limit: Maximum results
        exclude_domains: Domains to exclude from results

    Returns:
        List of (title, url, timestamp) tuples
    """
    cursor = conn.cursor()
    conditions: list[tuple[str, ...]] = [("url LIKE ?", f"%{domain}%")]

    if query:
        search_query = f"%{query}%"
        conditions.append(("title LIKE ? OR url LIKE ?", search_query, search_query))

    if exclude_domains:
        for exclude in exclude_domains:
            conditions.append(("url NOT LIKE ?", f"%{exclude}%"))

    sql, params = build_search_query(
        table="urls",
        columns=["title", "url", "last_visit_time"],
        conditions=conditions,
        order_by="last_visit_time",
        order_dir="DESC",
        limit=limit,
    )

    cursor.execute(sql, params)
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
    ]


def get_browser_stats(conn: sqlite3.Connection) -> dict[str, Any]:
    """
    Gets browsing statistics for the database.

    Args:
        conn: SQLite connection

    Returns:
        Dictionary with browsing statistics
    """
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM urls")
    total_entries = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(visit_count) FROM urls")
    total_visits = cursor.fetchone()[0] or 0

    cursor.execute("SELECT MAX(last_visit_time) FROM urls")
    last_visit_timestamp = cursor.fetchone()[0]
    last_visit = format_chrome_timestamp(last_visit_timestamp) if last_visit_timestamp else None

    cursor.execute("SELECT MIN(last_visit_time) FROM urls")
    first_visit_timestamp = cursor.fetchone()[0]
    first_visit = format_chrome_timestamp(first_visit_timestamp) if first_visit_timestamp else None

    cursor.execute("SELECT DISTINCT COUNT(*) FROM urls WHERE url LIKE 'http%'")
    unique_urls = cursor.fetchone()[0]

    return {
        "total_entries": total_entries,
        "total_visits": total_visits,
        "unique_urls": unique_urls,
        "first_visit": first_visit,
        "last_visit": last_visit,
    }


def get_most_visited_pages(conn: sqlite3.Connection, limit: int = 20) -> list[tuple[str, str, int]]:
    """
    Gets most visited individual pages (not just domains).

    Args:
        conn: SQLite connection
        limit: Maximum number of pages to return

    Returns:
        List of (title, url, visit_count) tuples
    """
    from chronicle_mcp.database.query import detect_schema, get_schema_columns

    schema = detect_schema(conn)
    if schema not in ("chrome", "firefox", "safari"):
        return []

    cols = get_schema_columns(schema)
    table = cols["table"]
    title_col = cols["title_col"]
    url_col = cols["url_col"]
    visit_count_col = cols["visit_count_col"]

    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {title_col}, {url_col}, {visit_count_col} FROM {table} WHERE {title_col} IS NOT NULL AND {url_col} LIKE 'http%' ORDER BY {visit_count_col} DESC LIMIT ?",
        (limit,),
    )
    return [(row[0], sanitize_url(row[1]), row[2]) for row in cursor.fetchall()]


def export_history(
    conn: sqlite3.Connection,
    format_type: str = "csv",
    limit: int = 1000,
    query: str | None = None,
) -> str:
    """
    Exports history to CSV or JSON format.

    Args:
        conn: SQLite connection
        format_type: 'csv' or 'json'
        limit: Maximum entries to export
        query: Optional search filter

    Returns:
        Formatted export string
    """
    import csv
    import json
    from io import StringIO

    from chronicle_mcp.database.query import detect_schema

    schema = detect_schema(conn)
    timestamp_formatter = {
        "chrome": format_chrome_timestamp,
        "firefox": format_firefox_timestamp,
        "safari": format_safari_timestamp,
    }.get(schema, format_chrome_timestamp)

    cursor = conn.cursor()
    params: list[str | int] = []
    sql = "SELECT title, url, last_visit_time FROM urls"

    if query:
        search_query = f"%{query}%"
        sql += " WHERE (title LIKE ? OR url LIKE ?)"
        params.extend([search_query, search_query])

    sql += " ORDER BY last_visit_time DESC LIMIT ?"
    params.append(limit)

    cursor.execute(sql, params)
    rows = [
        {"title": title, "url": sanitize_url(url), "timestamp": timestamp_formatter(ts)}
        for title, url, ts in cursor.fetchall()
    ]

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


def get_history_entries(conn: sqlite3.Connection, limit: int = 10000) -> list[dict[str, Any]]:
    """
    Gets all history entries from a browser database.

    Args:
        conn: SQLite connection
        limit: Maximum entries to retrieve

    Returns:
        List of dicts with 'title', 'url', 'last_visit_time' keys
    """
    from chronicle_mcp.database.query import detect_schema

    schema = detect_schema(conn)
    cursor = conn.cursor()

    if schema == "firefox":
        cursor.execute(
            "SELECT title, url, last_visit_date FROM moz_places WHERE url IS NOT NULL ORDER BY last_visit_date DESC LIMIT ?",
            (limit,),
        )
        return [
            {"title": title or "", "url": url, "last_visit_time": last_visit_date or 0}
            for title, url, last_visit_date in cursor.fetchall()
        ]
    elif schema == "safari":
        cursor.execute(
            "SELECT title, url, visit_time FROM history_items ORDER BY visit_time DESC LIMIT ?",
            (limit,),
        )
        return [
            {"title": title or "", "url": url, "last_visit_time": int(visit_time * 1000000)}
            for title, url, visit_time in cursor.fetchall()
        ]
    else:
        cursor.execute(
            "SELECT title, url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?",
            (limit,),
        )
        return [
            {"title": title, "url": url, "last_visit_time": last_visit_time}
            for title, url, last_visit_time in cursor.fetchall()
        ]


def insert_history_entries(
    conn: sqlite3.Connection,
    entries: list[dict[str, Any]],
    merge_strategy: str = "latest",
) -> int:
    """
    Inserts history entries into a browser database.

    Args:
        conn: SQLite connection
        entries: List of dicts with 'title', 'url', 'last_visit_time' keys
        merge_strategy: 'latest' (replace duplicates with newer) or 'merge' (keep all)

    Returns:
        Number of entries inserted
    """
    from chronicle_mcp.database.query import detect_schema

    if not entries:
        return 0

    schema = detect_schema(conn)
    cursor = conn.cursor()
    inserted = 0

    for entry in entries:
        title = entry.get("title", "")
        url = entry.get("url", "")
        last_visit_time = entry.get("last_visit_time", 0)

        if schema == "firefox":
            cursor.execute("SELECT visit_count FROM moz_places WHERE url = ?", (url,))
            row = cursor.fetchone()
            existing_count = row[0] if row else 0
            new_count = existing_count + 1 if merge_strategy == "latest" else 1
            cursor.execute(
                """
                INSERT OR REPLACE INTO moz_places (url, title, visit_count, last_visit_date)
                VALUES (?, ?, ?, ?)
                """,
                (url, title, new_count, last_visit_time),
            )
        elif schema == "safari":
            safari_timestamp = last_visit_time / 1000000.0
            cursor.execute("SELECT visit_count FROM history_items WHERE url = ?", (url,))
            row = cursor.fetchone()
            existing_count = row[0] if row else 0
            new_count = existing_count + 1 if merge_strategy == "latest" else 1
            cursor.execute(
                """
                INSERT OR REPLACE INTO history_items (title, url, visit_time, visit_count)
                VALUES (?, ?, ?, ?)
                """,
                (title, url, safari_timestamp, new_count),
            )
        else:
            if merge_strategy == "latest":
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO urls (title, url, last_visit_time, visit_count)
                    VALUES (?, ?, ?, COALESCE((SELECT visit_count FROM urls WHERE url = ?), 0) + 1)
                    """,
                    (title, url, last_visit_time, url),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO urls (title, url, last_visit_time, visit_count)
                    VALUES (?, ?, ?, 1)
                    """,
                    (title, url, last_visit_time),
                )
        inserted += 1

    conn.commit()
    return inserted


def sync_to_browser(
    target_db_path: str,
    entries: list[dict[str, Any]],
    merge_strategy: str = "latest",
) -> int:
    """
    Syncs history entries directly to a browser database file.

    This function writes entries directly to the browser database without using
    temporary files, which is the appropriate approach for sync operations.

    Args:
        target_db_path: Path to the target browser database
        entries: List of dicts with 'title', 'url', 'last_visit_time' keys
        merge_strategy: 'latest' (replace duplicates with newer) or 'merge' (keep all)

    Returns:
        Number of entries inserted

    Raises:
        ValueError: If target database is not a valid SQLite database with history table
    """
    from chronicle_mcp.database.query import insert_history_entries

    if not entries:
        return 0

    conn = sqlite3.connect(target_db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        has_history_table = any(t in tables for t in ["urls", "moz_places", "history_items"])
        if not has_history_table:
            raise ValueError(
                f"Target database at {target_db_path} does not contain a recognized history table. "
                f"Found tables: {tables}"
            )

        result = insert_history_entries(conn, entries, merge_strategy)
        return result
    finally:
        conn.close()


def search_with_regex(
    conn: sqlite3.Connection, pattern: str, limit: int = 20, timeout_seconds: float = 1.0
) -> list[tuple[str, str, str]]:
    """
    Searches history using regex patterns.

    Args:
        conn: SQLite connection
        pattern: Python regex pattern
        limit: Maximum results
        timeout_seconds: Maximum time to spend on regex matching

    Returns:
        List of (title, url, timestamp) tuples

    Raises:
        ValueError: If regex pattern is invalid
        TimeoutError: If regex matching exceeds timeout
    """
    cursor = conn.cursor()
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
        cursor.execute(
            "SELECT title, url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?",
            (limit * 3,),
        )
        matches = []
        timeout_flag = threading.Event()

        def timeout_handler() -> None:
            timeout_flag.set()

        timer = threading.Timer(timeout_seconds, timeout_handler)
        timer.start()

        try:
            for title, url, ts in cursor.fetchall():
                if timeout_flag.is_set():
                    raise TimeoutError("Regex matching exceeded time limit")
                if compiled.search(title or "") or compiled.search(url or ""):
                    matches.append((title, sanitize_url(url), format_chrome_timestamp(ts)))
                if len(matches) >= limit:
                    break
        finally:
            timer.cancel()
            timer.join()

        return matches
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")


def search_with_fuzzy(
    conn: sqlite3.Connection, query: str, threshold: float = 0.6, limit: int = 20
) -> list[tuple[str, str, str, float]]:
    """
    Searches history with fuzzy matching for typos.

    Args:
        conn: SQLite connection
        query: Search term to match
        threshold: Minimum similarity score (0-1)
        limit: Maximum results

    Returns:
        List of (title, url, timestamp, score) tuples
    """
    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute(
        "SELECT title, url, last_visit_time FROM urls WHERE title LIKE ? OR url LIKE ? ORDER BY last_visit_time DESC LIMIT ?",
        (search_query, search_query, limit * 3),
    )

    matches = []
    for title, url, ts in cursor.fetchall():
        score = fuzzy_match_score(query, title or "")
        if score >= threshold:
            matches.append((title, sanitize_url(url), format_chrome_timestamp(ts), round(score, 3)))
        elif url:
            score = fuzzy_match_score(query, url)
            if score >= threshold:
                matches.append(
                    (title, sanitize_url(url), format_chrome_timestamp(ts), round(score, 3))
                )

    matches.sort(key=lambda x: x[3], reverse=True)
    return matches[:limit]


def search_history_advanced(
    conn: sqlite3.Connection,
    query: str,
    limit: int = 20,
    exclude_domains: list[str] | None = None,
    sort_by: str = "date",
    use_regex: bool = False,
    use_fuzzy: bool = False,
    fuzzy_threshold: float = 0.6,
) -> list[tuple[str, str, str]]:
    """
    Advanced search with multiple options.

    Args:
        conn: SQLite connection
        query: Search term
        limit: Maximum results
        exclude_domains: Domains to exclude
        sort_by: 'date', 'visit_count', 'title'
        use_regex: Use regex matching
        use_fuzzy: Use fuzzy matching
        fuzzy_threshold: Minimum similarity for fuzzy matching

    Returns:
        List of (title, url, timestamp) tuples
    """
    if use_regex:
        return search_with_regex(conn, query, limit)

    if use_fuzzy:
        results = search_with_fuzzy(conn, query, fuzzy_threshold, limit)
        return [(title, url, ts) for title, url, ts, _ in results]

    cursor = conn.cursor()
    conditions: list[tuple[str, ...]] = [("(title LIKE ? OR url LIKE ?)", f"%{query}%", f"%{query}%")]

    if exclude_domains:
        for domain in exclude_domains:
            conditions.append(("url NOT LIKE ?", f"%{domain}%"))

    order_column, order_dir = {
        "date": ("last_visit_time", "DESC"),
        "visit_count": ("visit_count", "DESC"),
        "title": ("title", "ASC"),
    }.get(sort_by, ("last_visit_time", "DESC"))

    sql, params = build_search_query(
        table="urls",
        columns=["title", "url", "last_visit_time"],
        conditions=conditions,
        order_by=order_column,
        order_dir=order_dir,
        limit=limit,
    )

    cursor.execute(sql, params)
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
    ]


def query_history_universal(
    conn: sqlite3.Connection,
    query: str,
    limit: int = 10,
    schema: str | None = None,
) -> list[tuple[str, str, str]]:
    """
    Universal history query that works with any browser schema.

    Args:
        conn: SQLite connection
        query: Search term
        limit: Maximum results
        schema: Browser schema type (auto-detected if None)

    Returns:
        List of (title, url, timestamp) tuples
    """
    from chronicle_mcp.database.query import detect_schema as detect

    if schema is None:
        schema = detect(conn)

    cursor = conn.cursor()
    search_query = f"%{query}%"

    if schema == "chrome":
        cursor.execute(
            "SELECT title, url, last_visit_time FROM urls WHERE title LIKE ? OR url LIKE ? ORDER BY last_visit_time DESC LIMIT ?",
            (search_query, search_query, limit),
        )
        return [
            (title, sanitize_url(url), format_chrome_timestamp(ts))
            for title, url, ts in cursor.fetchall()
        ]

    elif schema == "firefox":
        cursor.execute(
            "SELECT p.title, p.url, v.visit_date FROM moz_places p JOIN moz_visits v ON p.id = v.place_id WHERE p.title LIKE ? OR p.url LIKE ? ORDER BY v.visit_date DESC LIMIT ?",
            (search_query, search_query, limit),
        )
        return [
            (title, sanitize_url(url), format_firefox_timestamp(ts))
            for title, url, ts in cursor.fetchall()
        ]

    elif schema == "safari":
        cursor.execute(
            "SELECT hi.title, hi.url, hv.visit_time FROM history_items hi JOIN history_visits hv ON hi.id = hv.history_item_id WHERE hi.title LIKE ? OR hi.url LIKE ? ORDER BY hv.visit_time DESC LIMIT ?",
            (search_query, search_query, limit),
        )
        return [
            (title, sanitize_url(url), format_safari_timestamp(ts))
            for title, url, ts in cursor.fetchall()
        ]

    else:
        raise ValueError(f"Unsupported browser schema: {schema}")
