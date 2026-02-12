"""ChronicleMCP - Browser history access for AI agents."""
__version__ = "1.1.0"

from chronicle_mcp.config import Config, load_config, logger, setup_logging
from chronicle_mcp.connection import (
    BrowserNotFoundError,
    BrowserPathNotFoundError,
    ConnectionError,
    DatabaseLockedError,
    PermissionError,
    cleanup_temp_file,
    execute_with_connection,
    get_history_connection,
)
from chronicle_mcp.database import (
    count_domain_visits,
    format_chrome_timestamp,
    format_results,
    get_top_domains,
    query_history,
    query_recent_history,
    sanitize_url,
    search_by_date,
)
from chronicle_mcp.paths import (
    BROWSER_PATHS,
    expand_path,
    find_glob_path,
    get_all_browser_paths,
    get_available_browsers,
    get_browser_path,
    get_os_name,
)

__all__ = [
    "BROWSER_PATHS",
    "get_os_name",
    "expand_path",
    "find_glob_path",
    "get_browser_path",
    "get_available_browsers",
    "get_all_browser_paths",
    "sanitize_url",
    "format_chrome_timestamp",
    "query_history",
    "query_recent_history",
    "count_domain_visits",
    "get_top_domains",
    "search_by_date",
    "format_results",
    "Config",
    "load_config",
    "setup_logging",
    "logger",
    "get_history_connection",
    "execute_with_connection",
    "cleanup_temp_file",
    "ConnectionError",
    "BrowserNotFoundError",
    "BrowserPathNotFoundError",
    "PermissionError",
    "DatabaseLockedError",
]
