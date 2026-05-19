"""Bookmark and download query operations.

This module provides functions for querying bookmarks and downloads
from various browser databases (Chrome, Firefox, Safari).
"""

import sqlite3
from typing import Any

from chronicle_mcp.database.timestamps import format_chrome_timestamp, format_firefox_timestamp


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
            (title, url)
            for title, url in bookmarks
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
    from chronicle_mcp.database.query import detect_schema

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
