import sqlite3
from urllib.parse import urlparse


def sanitize_url(url: str) -> str:
    """Removes sensitive query parameters from URLs."""
    parsed = urlparse(url)
    sensitive_params = {"token", "session", "key", "password", "auth", "sid", "access_token"}

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

        items = [{"title": title, "url": url, "timestamp": ts} for title, url, ts in rows]
        return json.dumps({"results": items, "count": len(items)})

    results = [f"- **{title}**\n  URL: {url}\n  Timestamp: {ts}" for title, url, ts in rows]
    return "\n\n".join(results)
