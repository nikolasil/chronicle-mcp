import re
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse


def sanitize_url(url: str) -> str:
    """Removes sensitive query parameters from URLs."""
    parsed = urlparse(url)
    sensitive_params = {
        "token",
        "session",
        "key",
        "password",
        "auth",
        "sid",
        "access_token",
        "api_key",
        "apikey",
        "api-secret",
        "secret",
        "api_token",
        "apitoken",
        "bearer",
        "jwt",
        "csrf",
        "xsrf",
        "nonce",
        "salt",
        "hash",
    }

    query_parts = []
    for part in parsed.query.split("&"):
        param = part.split("=")[0] if "=" in part else part
        if param.lower() not in sensitive_params:
            query_parts.append(part)

    safe_query = "&".join(query_parts)
    reconstructed = parsed._replace(query=safe_query)
    return reconstructed.geturl()


def format_chrome_timestamp(microseconds: int) -> str:
    """
    Converts Chrome's microseconds-since-1601-01-01 to ISO 8601 string.

    Args:
        microseconds: Chrome's last_visit_time value

    Returns:
        ISO 8601 formatted datetime string
    """
    try:
        from datetime import datetime, timedelta, timezone

        epoch_delta = timedelta(microseconds=microseconds)
        chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        dt = chrome_epoch + epoch_delta
        return dt.isoformat()
    except Exception:
        return f"microseconds={microseconds}"


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
    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute(
        "SELECT title, url, last_visit_time FROM urls WHERE title LIKE ? OR url LIKE ? ORDER BY last_visit_time DESC LIMIT ?",
        (search_query, search_query, limit),
    )
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
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
    from datetime import datetime, timedelta, timezone

    cursor = conn.cursor()
    chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    cutoff_microseconds = int((cutoff - chrome_epoch).total_seconds() * 1_000_000)

    cursor.execute(
        "SELECT title, url, last_visit_time FROM urls WHERE last_visit_time > ? ORDER BY last_visit_time DESC LIMIT ?",
        (cutoff_microseconds, limit),
    )
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
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
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(visit_count) FROM urls WHERE url LIKE ?", (f"%{domain}%",))
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
        WHERE url LIKE 'http%'
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

    cursor = conn.cursor()
    chrome_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)

    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)

        # Ensure both datetimes are timezone-aware (UTC)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)

        start_microseconds = int((start_dt - chrome_epoch).total_seconds() * 1_000_000)
        end_microseconds = int((end_dt - chrome_epoch).total_seconds() * 1_000_000)
    except ValueError:
        return []

    search_query = f"%{query}%"
    cursor.execute(
        """SELECT title, url, last_visit_time FROM urls
           WHERE (title LIKE ? OR url LIKE ?)
           AND last_visit_time >= ? AND last_visit_time <= ?
           ORDER BY last_visit_time DESC LIMIT ?""",
        (search_query, search_query, start_microseconds, end_microseconds, limit),
    )
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
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
    cursor = conn.cursor()
    search_query = f"%{query}%"
    cursor.execute(
        "DELETE FROM urls WHERE (title LIKE ? OR url LIKE ?) AND rowid IN (SELECT rowid FROM urls WHERE (title LIKE ? OR url LIKE ?) LIMIT ?)",
        (search_query, search_query, search_query, search_query, limit),
    )
    deleted_count = cursor.rowcount
    conn.commit()
    return deleted_count if deleted_count > 0 else 0


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
    params: list[str | int] = []
    sql_conditions = ["url LIKE ?"]
    params.append(f"%{domain}%")

    if query:
        search_query = f"%{query}%"
        sql_conditions.append("(title LIKE ? OR url LIKE ?)")
        params.extend([search_query, search_query])

    if exclude_domains:
        for exclude in exclude_domains:
            sql_conditions.append("url NOT LIKE ?")
            params.append(f"%{exclude}%")

    where_clause = " AND ".join(sql_conditions)
    # nosec B608 - where_clause is built from controlled literals, not user input
    sql = f"SELECT title, url, last_visit_time FROM urls WHERE {where_clause} ORDER BY last_visit_time DESC LIMIT ?"  # nosec B608
    params.append(limit)

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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, url, visit_count FROM urls WHERE title IS NOT NULL AND url LIKE 'http%' ORDER BY visit_count DESC LIMIT ?",
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
        {"title": title, "url": sanitize_url(url), "timestamp": format_chrome_timestamp(ts)}
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


def search_with_regex(
    conn: sqlite3.Connection, pattern: str, limit: int = 20
) -> list[tuple[str, str, str]]:
    """
    Searches history using regex patterns.

    Args:
        conn: SQLite connection
        pattern: Python regex pattern
        limit: Maximum results

    Returns:
        List of (title, url, timestamp) tuples
    """
    cursor = conn.cursor()
    try:
        compiled = re.compile(pattern, re.IGNORECASE)
        cursor.execute(
            "SELECT title, url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT ?",
            (limit,),
        )
        matches = []
        for title, url, ts in cursor.fetchall():
            if compiled.search(title or "") or compiled.search(url or ""):
                matches.append((title, sanitize_url(url), format_chrome_timestamp(ts)))
        return matches[:limit]
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")


def fuzzy_match_score(s1: str, s2: str) -> float:
    """
    Calculates fuzzy match similarity score between two strings.

    Args:
        s1: First string
        s2: Second string

    Returns:
        Similarity score between 0 and 1
    """
    if not s1 or not s2:
        return 0.0

    s1_lower = s1.lower()
    s2_lower = s2.lower()

    if s1_lower == s2_lower:
        return 1.0

    from difflib import SequenceMatcher

    score1 = SequenceMatcher(None, s1_lower, s2_lower).ratio()
    score2 = SequenceMatcher(None, s2_lower, s1_lower).ratio()

    return max(score1, score2)


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
    params: list[str | int] = []
    sql_conditions = ["(title LIKE ? OR url LIKE ?)"]
    params.append(f"%{query}%")
    params.append(f"%{query}%")

    if exclude_domains:
        for domain in exclude_domains:
            sql_conditions.append("url NOT LIKE ?")
            params.append(f"%{domain}%")

    where_clause = " AND ".join(sql_conditions)

    order_by = {
        "date": "last_visit_time DESC",
        "visit_count": "visit_count DESC",
        "title": "title ASC",
    }.get(sort_by, "last_visit_time DESC")

    # nosec B608 - both where_clause and order_by are built from controlled literals
    sql = f"SELECT title, url, last_visit_time FROM urls WHERE {where_clause} ORDER BY {order_by} LIMIT ?"  # nosec B608
    params.append(limit)

    cursor.execute(sql, params)
    return [
        (title, sanitize_url(url), format_chrome_timestamp(ts))
        for title, url, ts in cursor.fetchall()
    ]


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


def format_firefox_timestamp(microseconds: int) -> str:
    """
    Converts Firefox's microseconds-since-1970-01-01 to ISO 8601 string.

    Args:
        microseconds: Firefox's visit_date value

    Returns:
        ISO 8601 formatted datetime string
    """
    try:
        epoch_delta = timedelta(microseconds=microseconds)
        firefox_epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        dt = firefox_epoch + epoch_delta
        return dt.isoformat()
    except Exception:
        return f"microseconds={microseconds}"


def format_safari_timestamp(seconds: int) -> str:
    """
    Converts Apple's CFAbsoluteTime (seconds since 2001-01-01) to ISO 8601 string.

    Args:
        seconds: Safari's timestamp value

    Returns:
        ISO 8601 formatted datetime string
    """
    try:
        epoch_delta = timedelta(seconds=seconds)
        safari_epoch = datetime(2001, 1, 1, tzinfo=timezone.utc)
        dt = safari_epoch + epoch_delta
        return dt.isoformat()
    except Exception:
        return f"seconds={seconds}"


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
    if schema is None:
        schema = detect_schema(conn)

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


def query_bookmarks_chrome(
    bookmark_path: str, query: str | None = None, limit: int = 50
) -> list[tuple[str, str]]:
    """
    Queries Chrome-based browser bookmarks from JSON file.

    Args:
        bookmark_path: Path to Bookmarks JSON file
        query: Optional search term to filter bookmarks
        limit: Maximum number of results

    Returns:
        List of (title, url) tuples
    """
    import json

    bookmarks = []
    try:
        with open(bookmark_path, encoding="utf-8") as f:
            data = json.load(f)

        def extract_bookmarks(node: dict[str, Any]) -> None:
            if node.get("type") == "url":
                title = node.get("name", "")
                url = node.get("url", "")
                if title or url:
                    bookmarks.append((title, url))
            elif node.get("type") == "folder":
                for child in node.get("children", []):
                    extract_bookmarks(child)

        for root in data.get("roots", {}).values():
            if isinstance(root, dict):
                extract_bookmarks(root)

    except (OSError, json.JSONDecodeError):
        return []

    if query:
        query_lower = query.lower()
        bookmarks = [
            (title, url) for title, url in bookmarks
            if query_lower in (title or "").lower() or query_lower in (url or "").lower()
        ]

    return bookmarks[:limit]


def query_bookmarks_firefox(
    conn: sqlite3.Connection, query: str | None = None, limit: int = 50
) -> list[tuple[str, str]]:
    """
    Queries Firefox bookmarks from places.sqlite.

    Args:
        conn: SQLite connection to places.sqlite
        query: Optional search term to filter bookmarks
        limit: Maximum number of results

    Returns:
        List of (title, url) tuples
    """
    cursor = conn.cursor()

    if query:
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT p.title, p.url FROM moz_bookmarks b JOIN moz_places p ON b.fk = p.id WHERE p.title LIKE ? OR p.url LIKE ? LIMIT ?",
            (search_query, search_query, limit),
        )
    else:
        cursor.execute(
            "SELECT p.title, p.url FROM moz_bookmarks b JOIN moz_places p ON b.fk = p.id LIMIT ?",
            (limit,),
        )

    return [(title, url) for title, url in cursor.fetchall() if url]


def query_downloads_chrome(
    conn: sqlite3.Connection, query: str | None = None, limit: int = 50
) -> list[tuple[str, str, str]]:
    """
    Queries downloads from Chrome-based browser history database.

    Args:
        conn: SQLite connection to History database
        query: Optional search term to filter downloads
        limit: Maximum number of results

    Returns:
        List of (filename, url, timestamp) tuples
    """
    cursor = conn.cursor()

    if query:
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT filename, url, start_time FROM downloads WHERE filename LIKE ? OR url LIKE ? ORDER BY start_time DESC LIMIT ?",
            (search_query, search_query, limit),
        )
    else:
        cursor.execute(
            "SELECT filename, url, start_time FROM downloads ORDER BY start_time DESC LIMIT ?",
            (limit,),
        )

    return [
        (filename, url, format_chrome_timestamp(start_time))
        for filename, url, start_time in cursor.fetchall()
        if filename
    ]


def query_downloads_firefox(
    conn: sqlite3.Connection, query: str | None = None, limit: int = 50
) -> list[tuple[str, str, str]]:
    """
    Queries downloads from Firefox places.sqlite.

    Args:
        conn: SQLite connection to places.sqlite
        query: Optional search term to filter downloads
        limit: Maximum number of results

    Returns:
        List of (filename, url, timestamp) tuples
    """
    cursor = conn.cursor()

    if query:
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT p.title, p.url, v.visit_date FROM moz_places p JOIN moz_visits v ON p.id = v.place_id JOIN moz_downloads d ON p.id = d.place_id WHERE p.title LIKE ? OR p.url LIKE ? ORDER BY v.visit_date DESC LIMIT ?",
            (search_query, search_query, limit),
        )
    else:
        cursor.execute(
            "SELECT p.title, p.url, v.visit_date FROM moz_places p JOIN moz_visits v ON p.id = v.place_id JOIN moz_downloads d ON p.id = d.place_id ORDER BY v.visit_date DESC LIMIT ?",
            (limit,),
        )

    return [
        (title, url, format_firefox_timestamp(visit_date))
        for title, url, visit_date in cursor.fetchall()
        if url
    ]


def query_bookmarks(
    bookmark_path: str | None,
    schema: str = "chrome",
    query: str | None = None,
    limit: int = 50,
) -> list[tuple[str, str]]:
    """
    Universal bookmark query that works with any browser.

    Args:
        bookmark_path: Path to bookmarks file/database
        schema: Browser schema type (chrome, firefox, safari)
        query: Optional search term
        limit: Maximum results

    Returns:
        List of (title, url) tuples
    """
    if not bookmark_path:
        return []

    if schema == "firefox":
        import glob as g
        import os

        expanded = os.path.expanduser(os.path.expandvars(bookmark_path))
        if "*" in expanded:
            matches = g.glob(expanded)
            if not matches:
                return []
            bookmark_path = matches[0]

        conn = sqlite3.connect(bookmark_path)
        try:
            return query_bookmarks_firefox(conn, query, limit)
        finally:
            conn.close()
    else:
        return query_bookmarks_chrome(bookmark_path, query, limit)


def query_downloads(
    download_path: str | None,
    schema: str = "chrome",
    query: str | None = None,
    limit: int = 50,
) -> list[tuple[str, str, str]]:
    """
    Universal downloads query that works with any browser.

    Args:
        download_path: Path to downloads database
        schema: Browser schema type (chrome, firefox, safari)
        query: Optional search term
        limit: Maximum results

    Returns:
        List of (filename, url, timestamp) tuples
    """
    if not download_path:
        return []

    import glob as g
    import os

    expanded = os.path.expanduser(os.path.expandvars(download_path))
    if "*" in expanded:
        matches = g.glob(expanded)
        if not matches:
            return []
        download_path = matches[0]

    try:
        conn = sqlite3.connect(download_path)
        try:
            detected_schema = detect_schema(conn)
            if detected_schema == "firefox" or schema == "firefox":
                return query_downloads_firefox(conn, query, limit)
            else:
                return query_downloads_chrome(conn, query, limit)
        finally:
            conn.close()
    except sqlite3.OperationalError:
        return []
