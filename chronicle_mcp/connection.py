"""Database connection management for ChronicleMCP.

This module provides a centralized way to connect to browser history databases
while avoiding 'Database Locked' errors by using temporary copies.
"""

import logging
import os
import shutil
import sqlite3
import tempfile
import time
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Callable

from chronicle_mcp.paths import get_browser_path

logger = logging.getLogger(__name__)


class ConnectionError(Exception):
    """Base exception for connection errors."""

    def __init__(self, message: str, browser: str, details: str | None = None):
        self.message = message
        self.browser = browser
        self.details = details
        super().__init__(self.message)


class BrowserNotFoundError(ConnectionError):
    """Raised when the specified browser's history is not found."""

    def __init__(self, browser: str):
        super().__init__(
            message=f"Could not find {browser} history",
            browser=browser,
            details=f"Ensure {browser} is installed and has history data",
        )


class BrowserPathNotFoundError(ConnectionError):
    """Raised when the browser's history path doesn't exist."""

    def __init__(self, browser: str, path: str):
        super().__init__(
            message=f"Could not find {browser} history at {path}",
            browser=browser,
            details="Check that the path exists and is accessible",
        )


class PermissionError(ConnectionError):
    """Raised when permission is denied accessing the history database."""

    def __init__(self, browser: str, path: str):
        super().__init__(
            message=f"Permission denied accessing {browser} history at {path}",
            browser=browser,
            details="Ensure the browser is closed and you have read permissions",
        )


class DatabaseLockedError(ConnectionError):
    """Raised when the database is locked (browser is open)."""

    def __init__(self, browser: str, path: str):
        super().__init__(
            message=f"Unable to access {browser} history database (locked)",
            browser=browser,
            details="Ensure the browser is closed before querying",
        )


def get_temp_filename(browser: str) -> str:
    """Generate a unique temporary filename for the database copy.

    Args:
        browser: Browser name for identification

    Returns:
        Path string for the temporary file
    """
    temp_dir = tempfile.gettempdir()
    return os.path.join(
        temp_dir,
        f"chronicle_{browser}_temp_{os.getpid()}_{int(time.time() * 1000)}.db",
    )


def cleanup_temp_file(temp_path: str) -> None:
    """Safely remove a temporary database file.

    Args:
        temp_path: Path to the temporary file to remove
    """
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.debug(f"Cleaned up temp file: {temp_path}")
    except OSError as e:
        logger.warning(f"Failed to clean up temp file {temp_path}: {e}")


@contextmanager
def get_history_connection(
    browser: str = "chrome",
) -> Generator[sqlite3.Connection, None, None]:
    """Creates a temporary copy of the history database to avoid 'Database Locked' errors.

    This function copies the browser's history database to a temporary file,
    opens it, and ensures cleanup after the context exits. This prevents
    database locking issues when the browser is running.

    Args:
        browser: Browser name (chrome, edge, firefox) - case insensitive

    Yields:
        SQLite connection to the history database

    Raises:
        BrowserNotFoundError: If the browser is not recognized
        BrowserPathNotFoundError: If the history path doesn't exist
        PermissionError: If the file cannot be read
        DatabaseLockedError: If the database is locked
    """
    browser_lower = browser.lower()

    history_path = get_browser_path(browser_lower)

    if not history_path:
        raise BrowserNotFoundError(browser_lower)

    if not os.path.exists(history_path):
        raise BrowserPathNotFoundError(browser_lower, history_path)

    temp_path = get_temp_filename(browser_lower)

    try:
        logger.debug(f"Copying {browser} history to temp file: {temp_path}")
        shutil.copy2(history_path, temp_path)

        conn = sqlite3.connect(temp_path)
        try:
            yield conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                raise DatabaseLockedError(browser_lower, history_path) from e
            raise
        finally:
            conn.close()
            cleanup_temp_file(temp_path)

    except PermissionError:
        raise
    except OSError as e:
        if "permission" in str(e).lower():
            raise PermissionError(browser_lower, history_path) from e
        cleanup_temp_file(temp_path)
        raise ConnectionError(
            f"Failed to access {browser} history: {e}",
            browser=browser_lower,
            details=str(e),
        ) from e
    except Exception:
        cleanup_temp_file(temp_path)
        raise


def execute_with_connection(browser: str, func: Callable[[sqlite3.Connection], Any]) -> Any:
    """Execute a function with a database connection.

    This is a convenience function for synchronous operations that need
    a database connection without using the context manager pattern.

    Args:
        browser: Browser name
        func: Function to execute with the connection

    Returns:
        Result of the function execution

    Raises:
        ConnectionError: Any connection-related error
    """
    with get_history_connection(browser) as conn:
        return func(conn)
