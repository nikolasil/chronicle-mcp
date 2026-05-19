"""Safe SQL query builder utilities.

This module provides utilities for building SQL queries safely using
parameterized queries rather than string interpolation. It helps prevent
SQL injection vulnerabilities by ensuring user input always goes through
SQLite parameter binding.
"""

from typing import Any


class SqlBuilder:
    """Builder for safe SQL queries using parameterized values."""

    def __init__(self, base_query: str):
        """Initialize with a base query template.

        Args:
            base_query: SQL query with placeholders for parameters
        """
        self._query = base_query
        self._params: list[Any] = []

    def where(self, condition: str, *values: Any) -> "SqlBuilder":
        """Add a WHERE condition with parameterized values.

        Args:
            condition: SQL condition using ? placeholders
            values: Values to bind to the condition

        Returns:
            Self for chaining
        """
        if not hasattr(self, "_where_clauses"):
            self._where_clauses: list[str] = []
        self._where_clauses.append(condition)
        self._params.extend(values)
        return self

    def order_by(self, column: str, direction: str = "ASC") -> "SqlBuilder":
        """Add ORDER BY clause.

        Args:
            column: Column name (should be validated before use)
            direction: Sort direction (ASC or DESC)

        Returns:
            Self for chaining
        """
        direction = direction.upper()
        if direction not in ("ASC", "DESC"):
            direction = "ASC"
        self._order_column = column
        self._order_direction = direction
        return self

    def limit(self, count: int) -> "SqlBuilder":
        """Add LIMIT clause.

        Args:
            count: Maximum number of results

        Returns:
            Self for chaining
        """
        self._limit = count
        return self

    def build(self) -> tuple[str, list[Any]]:
        """Build the final SQL query and parameters.

        Returns:
            Tuple of (sql_string, params_list)
        """
        query = self._query
        params = list(self._params)

        where_clause = getattr(self, "_where_clauses", None)
        if where_clause:
            where_str = " AND ".join(where_clause)
            query = f"{query} WHERE {where_str}"

        order_column = getattr(self, "_order_column", None)
        if order_column:
            order_dir = getattr(self, "_order_direction", "ASC")
            query = f"{query} ORDER BY {order_column} {order_dir}"

        limit = getattr(self, "_limit", None)
        if limit is not None:
            query = f"{query} LIMIT ?"
            params.append(limit)

        return query, params


def build_search_query(
    table: str,
    columns: list[str],
    conditions: list[tuple[str, ...]],
    order_by: str | None = None,
    order_dir: str = "DESC",
    limit: int | None = None,
) -> tuple[str, list[Any]]:
    """Build a SELECT query safely with parameterized conditions.

    Args:
        table: Table name (should be validated before use)
        columns: List of column names to select
        conditions: List of (condition_sql, *values) tuples
        order_by: Column to order by (optional)
        order_dir: Sort direction (ASC or DESC)
        limit: Maximum results (optional)

    Returns:
        Tuple of (sql_string, params_list)

    Example:
        >>> query, params = build_search_query(
        ...     table="urls",
        ...     columns=["title", "url", "last_visit_time"],
        ...     conditions=[
        ...         ("title LIKE ? OR url LIKE ?", "%python%", "%python%"),
        ...         ("domain NOT LIKE ?", "%evil%"),
        ...     ],
        ...     order_by="last_visit_time",
        ...     limit=20
        ... )
    """
    col_str = ", ".join(columns)
    query = f"SELECT {col_str} FROM {table}"

    if conditions:
        where_parts = []
        params: list[Any] = []
        for cond in conditions:
            if isinstance(cond, str):
                where_parts.append(cond)
            else:
                where_parts.append(cond[0])
                params.extend(cond[1:])
        query = f"{query} WHERE {' AND '.join(where_parts)}"

    if order_by:
        direction = order_dir.upper() if order_dir.upper() in ("ASC", "DESC") else "DESC"
        query = f"{query} ORDER BY {order_by} {direction}"

    if limit is not None:
        query = f"{query} LIMIT ?"
        params.append(limit)

    return query, params


def build_delete_query(
    table: str,
    conditions: list[tuple[str, ...]],
) -> tuple[str, list[Any]]:
    """Build a DELETE query safely with parameterized conditions.

    Args:
        table: Table name (should be validated before use)
        conditions: List of (condition_sql, *values) tuples

    Returns:
        Tuple of (sql_string, params_list)
    """
    query = f"DELETE FROM {table}"

    if conditions:
        where_parts = []
        params: list[Any] = []
        for cond in conditions:
            if isinstance(cond, str):
                where_parts.append(cond)
            else:
                where_parts.append(cond[0])
                params.extend(cond[1:])
        query = f"{query} WHERE {' AND '.join(where_parts)}"

    return query, params
