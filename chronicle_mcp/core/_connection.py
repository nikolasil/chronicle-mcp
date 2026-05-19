"""Connection helper for service layer.

This module provides a reusable with_connection helper that handles
database connection lifecycle and exception mapping.
"""

import logging
from collections.abc import Callable
from typing import Any

from chronicle_mcp.core.exceptions import (
    BrowserNotFoundError,
    BrowserPathNotFoundError,
    DatabaseError,
    DatabaseLockedError,
    PermissionDeniedError,
)

logger = logging.getLogger(__name__)

# Module-level reference to get_history_connection, can be patched by tests
from chronicle_mcp.connection import get_history_connection as _get_history_connection_func

_get_history_connection = _get_history_connection_func


def with_connection(browser: str, operation: Callable[..., Any]) -> Any:
    """Execute an operation with a database connection.

    Args:
        browser: Browser name
        operation: Function that takes a connection and returns data

    Returns:
        Result of the operation

    Raises:
        BrowserNotFoundError: If browser not found
        BrowserPathNotFoundError: If path not found
        DatabaseLockedError: If database is locked
        PermissionDeniedError: If permission denied
        DatabaseError: For other database errors
    """
    from chronicle_mcp.connection import (
        BrowserNotFoundError as ConnBrowserNotFoundError,
    )
    from chronicle_mcp.connection import (
        BrowserPathNotFoundError as ConnBrowserPathNotFoundError,
    )
    from chronicle_mcp.connection import (
        ConnectionError as ConnConnectionError,
    )
    from chronicle_mcp.connection import (
        DatabaseLockedError as ConnDatabaseLockedError,
    )
    from chronicle_mcp.connection import (
        PermissionDeniedError as ConnPermissionDeniedError,
    )

    try:
        with _get_history_connection(browser) as conn:
            return operation(conn)
    except ConnBrowserNotFoundError:
        raise BrowserNotFoundError(browser)
    except ConnBrowserPathNotFoundError:
        raise BrowserPathNotFoundError(browser, "")
    except ConnDatabaseLockedError:
        raise DatabaseLockedError(browser)
    except ConnPermissionDeniedError:
        raise PermissionDeniedError(browser, "")
    except ConnConnectionError as e:
        logger.error(f"Connection error: {e.message}")
        raise DatabaseError(f"Failed to access {browser} history: {e.message}")
    except Exception as e:
        logger.exception("Unexpected database error")
        raise DatabaseError(f"Database operation failed: {e}")
