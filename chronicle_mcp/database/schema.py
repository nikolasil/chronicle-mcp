import sqlite3


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
