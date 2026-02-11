import os
import glob
import platform
from typing import Optional, Dict, List


BROWSER_PATHS: Dict[str, Dict[str, str]] = {
    "chrome": {
        "Windows": r"%LocalAppData%\Google\Chrome\User Data\Default\History",
        "Darwin": "~/Library/Application Support/Google/Chrome/Default/History",
        "Linux": "~/.config/google-chrome/Default/History"
    },
    "edge": {
        "Windows": r"%LocalAppData%\Microsoft\Edge\User Data\Default\History",
        "Darwin": "~/Library/Application Support/Microsoft Edge/Default/History",
        "Linux": "~/.config/microsoft-edge/Default/History"
    },
    "firefox": {
        "Windows": r"%AppData%\Mozilla\Firefox\Profiles\*.default\places.sqlite",
        "Darwin": "~/Library/Mozilla/Firefox/Profiles/*.default/places.sqlite",
        "Linux": "~/.mozilla/firefox/*.default/places.sqlite"
    }
}


def get_os_name() -> str:
    """Returns the current operating system name."""
    return platform.system()


def expand_path(path: str) -> str:
    """Expands environment variables and home directory in path."""
    return os.path.expandvars(os.path.expanduser(path))


def find_glob_path(pattern: str) -> Optional[str]:
    """Finds a file matching the glob pattern, returns first match or None."""
    matches = glob.glob(expand_path(pattern))
    return matches[0] if matches else None


def get_browser_path(browser: str) -> Optional[str]:
    """
    Gets the history database path for the specified browser.

    Args:
        browser: Browser name (chrome, edge, firefox) - case insensitive

    Returns:
        Path to history database or None if not found
    """
    browser_lower = browser.lower()

    if browser_lower not in BROWSER_PATHS:
        return None

    os_name = get_os_name()
    path_pattern = BROWSER_PATHS[browser_lower].get(os_name)

    if not path_pattern:
        return None

    if "*" in path_pattern:
        return find_glob_path(path_pattern)
    else:
        expanded = expand_path(path_pattern)
        return expanded if os.path.exists(expanded) else None


def get_available_browsers() -> List[str]:
    """
    Returns a list of browsers with detected history databases.
    """
    available = []
    for browser in BROWSER_PATHS:
        if get_browser_path(browser):
            available.append(browser)
    return available


def get_all_browser_paths() -> Dict[str, Optional[str]]:
    """
    Returns a dictionary of all browser paths (found or not found).
    Useful for debugging.
    """
    result = {}
    for browser in BROWSER_PATHS:
        path = get_browser_path(browser)
        result[browser] = path
    return result
